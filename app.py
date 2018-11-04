import os

import pandas as pd
import numpy as np
import sqlalchemy
import pymysql
import json
#import csv
import model_info

from flask import Flask
from flask import jsonify
from flask import request
from flask import make_response
from flask import url_for
from flask import render_template

from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import sessionmaker
#from sqlalchemy.pool import SingletonThreadPool


pymysql.install_as_MySQLdb()

app = Flask(__name__, static_folder='public', static_url_path='')

#################################################
# Database Setup
#################################################

# Database Connection
#username = 'root'
#password = 'ming1119'
#host = 'localhost'
#port = '3306'
#database = 'big_mart_db'

# setup engine
engine = create_engine("mysql://root:ming1119@localhost:3306/big_mart_db")
#engine = create_engine("sqlite:///db/big_mart_db.db",poolclass=SingletonThreadPool)
# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)
# Create our session (link) from Python to the DB
Session = sessionmaker(bind=engine)

# Save references to db table
Train_data = Base.classes.train_tb
Test_data = Base.classes.test_tb

#################################################
# Route Setup
#################################################

#Return the homepage
@app.route("/")
def index():
    return render_template("index.html")

#Return the machine learning model page
@app.route("/ml_model")
def ml_model():
    return render_template("ml_model.html")
# possible api routes:
# /api/data/train
# /api/data/test
# /api/data/train/stats
# /api/data/train/corr


#Return all data from train data table
@app.route("/api/data/train")
def train_data():

    #open session for querying the data from sqlite
    session = Session()
    #querying train table from sqlite
    train_results = session.query(Train_data.key, Train_data.item_fat_content,Train_data.item_identifier, Train_data.item_MRP
                             ,Train_data.item_outlet_sales,Train_data.item_type, Train_data.item_weight, Train_data.outlet_identifier
                             ,Train_data.outlet_location_type,Train_data.outlet_size,Train_data.outlet_type,Train_data.source
                             ,Train_data.outlet_years,Train_data.item_visibility_mean_ratio).all()
    #close session
    session.close()

    #convert sql result to df
    train_df = pd.DataFrame(train_results)

    #jsonfy the df
    train_json = json.loads(train_df.to_json(orient='records'))

    #return with json format data for api
    return jsonify(train_json)

#Return all data from test data table
@app.route("/api/data/test")
def test_data():

    #open session for querying the data from sqlite
    session = Session()
    #querying train table from sqlite
    test_results = session.query(Test_data.key, Test_data.item_fat_content,Test_data.item_identifier, Test_data.item_MRP
                             ,Test_data.item_outlet_sales,Test_data.item_type, Test_data.item_weight, Test_data.outlet_identifier
                             ,Test_data.outlet_location_type,Test_data.outlet_size,Test_data.outlet_type,Test_data.source
                             ,Test_data.outlet_years,Test_data.item_visibility_mean_ratio).all()
    #close session
    session.close()

    #convert sql result to df
    test_df = pd.DataFrame(test_results)

    #jsonfy the df
    test_json = json.loads(test_df.to_json(orient='records'))

    #return with json format data for api
    return jsonify(test_json)


#Return stats summary of test data
@app.route("/api/data/train/summary")
def train_summary():

#open session for querying the data from sqlite
    session = Session()
    #querying train table from sqlite
    train_results = session.query(Train_data.item_MRP,Train_data.item_outlet_sales,Train_data.item_weight 
                             ,Train_data.outlet_years,Train_data.item_visibility_mean_ratio).all()
    #close session
    session.close()

    #convert sql result to df
    train_df = pd.DataFrame(train_results)
    #convert all column data type into numeric/float
    train_df[['item_MRP','item_outlet_sales','item_weight','outlet_years','item_visibility_mean_ratio']] = train_df[['item_MRP','item_outlet_sales','item_weight'
                                                                                                                    ,'outlet_years','item_visibility_mean_ratio']].astype(float)

    #summary of train data
    train_summary = train_df.describe(include = 'all')
    #reset index in order to stats column
    train_summary = train_summary.reset_index()
    #rename index to stats
    train_summary.rename(columns={'index': 'stats'}, inplace=True)

    train_summary_json = json.loads(train_summary.to_json(orient='records'))
     
    return jsonify(train_summary_json)


#Return correlation of test data
@app.route("/api/data/train/corr")
def train_corr():

#open session for querying the data from sqlite
    session = Session()
    #querying train table from sqlite
    train_results = session.query(Train_data.item_MRP,Train_data.item_outlet_sales,Train_data.item_weight 
                             ,Train_data.outlet_years,Train_data.item_visibility_mean_ratio).all()
    #close session
    session.close()

    #convert sql result to df
    train_df = pd.DataFrame(train_results)
    #convert all column data type into numeric/float
    train_df[['item_MRP','item_outlet_sales','item_weight','outlet_years','item_visibility_mean_ratio']] = train_df[['item_MRP','item_outlet_sales','item_weight'
                                                                                                                    ,'outlet_years','item_visibility_mean_ratio']].astype(float)

    #summary of train data
    train_corr = train_df.corr()
    #reset index in order to stats column
    train_corr = train_corr.reset_index()
    #rename index to stats
    train_corr.rename(columns={'index': 'stats'}, inplace=True)


    train_corr_json = json.loads(train_corr.to_json(orient='records'))
     
    return jsonify(train_corr_json)

#return each outlet's sales information
@app.route("/api/data/train/avg_item_sales")
def outlet_sales():

    #total sales for store column
    total_sales = func.sum(Train_data.item_outlet_sales)
    #total item quantity sold in entire store column
    total_items_sold = func.sum(Train_data.item_outlet_sales/Train_data.item_MRP)
    #average sale per item for entire store column
    avg_sale_per_item = total_sales/total_items_sold

    #columns queried
    columns = (Train_data.outlet_identifier, Train_data.outlet_type, total_sales, total_items_sold, avg_sale_per_item)
    
    #open session for querying the data from sqlite
    session = Session()
    #query
    query = session.query(*columns).filter(Train_data.source=="train").group_by(Train_data.outlet_identifier)
    #close session after query
    session.close()
    
    stores = []
    dict = {}

    #create dictionary of queried data
    for a, b, c, d, e in query:
        dict = {"outlet_id": a, "outlet_type": b, "total_sales": "{:.2f}".format(c), 
                "quantity_sold": int(d), "avg_sale_per_item": "{:.2f}".format(e)}
        stores.append(dict)

    return jsonify(stores)

#return top 10 item sales information
@app.route("/api/data/train/top_10_items")
def item_sales():

    #quantity of items sold for unique product
    item_quantity = Train_data.item_outlet_sales/Train_data.item_MRP

    #columns in query
    columns = (Train_data.outlet_identifier, Train_data.item_identifier, Train_data.item_type, Train_data.item_visibility_mean_ratio, Train_data.item_MRP
                    , Train_data.item_outlet_sales, item_quantity)

    #open session 
    session = Session()
    #query
    query = session.query(*columns).filter(Train_data.source=="train").order_by(Train_data.item_outlet_sales.desc()).limit(10)
    #close session after query
    session.close()

    list = []
    dict2 = {}

    #create dictionary of queried data
    for a, b, c, d, e, f, g in query:
        dict2 = {"outlet_id": a, "item_id": b, "item_type": c, "item_visibility": "{:.5f}".format(d), 
                "item_max_retail_price": "{:.2f}".format(e), "total_item_sales": "{:.2f}".format(f),
               "total_quantity_sold": int(g)}
        list.append(dict2)

    return jsonify(list)


#Return ml model's R^2 and RMSE
@app.route("/api/data/models/summary")
def model_stats():

    #open session for querying the data from sqlite
    session = Session()
    #querying train table from sqlite
    train_results = session.query(Train_data.key, Train_data.item_fat_content,Train_data.item_identifier, Train_data.item_MRP
                             ,Train_data.item_outlet_sales,Train_data.item_type, Train_data.item_weight, Train_data.outlet_identifier
                             ,Train_data.outlet_location_type,Train_data.outlet_size,Train_data.outlet_type,Train_data.source
                             ,Train_data.outlet_years,Train_data.item_visibility_mean_ratio).all()
    #close session
    session.close()

    #convert sql result to df
    train_df = pd.DataFrame(train_results)

    #call linear regression summary
    linear_regression = model_info.sklearn_model(train_df)
    #call ridge regression summary
    ridge_regression = model_info.ridge_model(train_df)
    #call lasso regression summary
    lasso_regression = model_info.lasso_model(train_df)
    #call decision tree summary
    decision_tree = model_info.dec_tree_model(train_df)

    #union all dataframes
    model_summary_df = pd.concat([linear_regression,ridge_regression,lasso_regression,decision_tree],ignore_index = True)

    #jsonfy dataframes
    model_summary_json = json.loads(model_summary_df.to_json(orient='records'))

    return jsonify(model_summary_json)


#Return decision tree prediction
@app.route("/api/data/models/dec_tree/prediction")
def dec_tree_predict():

    #open session for querying the data from sqlite
    session = Session()
    #querying train table from sqlite
    train_results = session.query(Train_data.key, Train_data.item_fat_content,Train_data.item_identifier, Train_data.item_MRP
                             ,Train_data.item_outlet_sales,Train_data.item_type, Train_data.item_weight, Train_data.outlet_identifier
                             ,Train_data.outlet_location_type,Train_data.outlet_size,Train_data.outlet_type,Train_data.source
                             ,Train_data.outlet_years,Train_data.item_visibility_mean_ratio).all()

    test_results = session.query(Test_data.key, Test_data.item_fat_content,Test_data.item_identifier, Test_data.item_MRP
                             ,Test_data.item_outlet_sales,Test_data.item_type, Test_data.item_weight, Test_data.outlet_identifier
                             ,Test_data.outlet_location_type,Test_data.outlet_size,Test_data.outlet_type,Test_data.source
                             ,Test_data.outlet_years,Test_data.item_visibility_mean_ratio).all()
    #close session
    session.close()

    #convert sql result to df
    train_df = pd.DataFrame(train_results)
    test_df = pd.DataFrame(test_results)

    #call decision tree prediction
    dec_tree_prediction = model_info.dec_tree_prediction(train_df,test_df)
    
    #jsonfy dataframes
    dec_tree_prediction_json = json.loads(dec_tree_prediction.to_json(orient='records'))

    return jsonify(dec_tree_prediction_json)

#################################################
# End of Route setup
#################################################

if __name__ == "__main__":
    app.run(debug=True)

