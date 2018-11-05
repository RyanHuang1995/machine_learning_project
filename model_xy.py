import os

import pandas as pd
import numpy as np
#import sqlalchemy
#import pymysql
import json
#import csv

#from flask import Flask
#from flask import jsonify
#from flask import request
#from flask import make_response
#from flask import url_for
#from flask import render_template

#from sqlalchemy.orm.exc import NoResultFound
#from sqlalchemy.orm import Session
#from sqlalchemy import create_engine, func
#from sqlalchemy.ext.automap import automap_base
#from sqlalchemy.orm import sessionmaker
from sklearn.linear_model import LinearRegression,Ridge,Lasso
from sklearn.model_selection import train_test_split
from sklearn import cross_validation, metrics
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import cross_val_score
from sklearn.linear_model import LinearRegression,Ridge,Lasso
from sklearn.model_selection import train_test_split
from sklearn import cross_validation, metrics
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import cross_val_score
from sklearn.tree import DecisionTreeRegressor
#from sqlalchemy.pool import SingletonThreadPool


#pymysql.install_as_MySQLdb()


###########################################################
# calculate model x and y for linear regression model
###########################################################
def linear_xy_model(train_df):

    #convert train_df into model data
    model_data = train_df[["item_outlet_sales","item_MRP","item_fat_content","item_type","outlet_location_type","outlet_size","outlet_type"]]
    # One-hot Coding
    model_data = pd.get_dummies(model_data, columns = ["item_fat_content","item_type","outlet_location_type","outlet_size","outlet_type"])
    # float conversion
    model_data['item_outlet_sales'] = model_data['item_outlet_sales'].astype(float)

    #sklearn x & y tune-up
    Y = model_data["item_outlet_sales"].values
    X = model_data.drop("item_outlet_sales",axis = 1).values
    Y = Y.reshape(-1,1)
    # Split train and test data
    X_train,X_test,y_train,y_test = train_test_split(X,Y,test_size = 0.3,random_state = 42)

    #Linear Regression
    reg_all = LinearRegression()
    reg_all.fit(X_train,y_train)
    y_pred = reg_all.predict(X_test)
    # Compute x and y into array
    predict_x = [x[0] for x in y_pred.astype(float)]
    actual_y = [y[0] for y in y_test.astype(float)]

    linear_xy_df = pd.DataFrame({'x': predict_x,'y':actual_y,'model':'linear_regression'})

    return linear_xy_df

###########################################################
# calculate model x and y for ridge regression model
###########################################################
def ridge_xy_model(train_df):

    #convert train_df into model data
    model_data = train_df[["item_outlet_sales","item_MRP","item_fat_content","item_type","outlet_location_type","outlet_size","outlet_type"]]
    # One-hot Coding
    model_data = pd.get_dummies(model_data, columns = ["item_fat_content","item_type","outlet_location_type","outlet_size","outlet_type"])
    # float conversion
    model_data['item_outlet_sales'] = model_data['item_outlet_sales'].astype(float)

    #sklearn x & y tune-up
    Y = model_data["item_outlet_sales"].values
    X = model_data.drop("item_outlet_sales",axis = 1).values
    Y = Y.reshape(-1,1)
    # Split train and test data
    X_train,X_test,y_train,y_test = train_test_split(X,Y,test_size = 0.3,random_state = 42)

    #Ridge Regression
    ridge = Ridge(alpha = 0.05,normalize = True)
    # fit the model
    ridge.fit(X_train,y_train)
    y_pred = ridge.predict(X_test)

    # Compute x and y into array
    predict_x = [x[0] for x in y_pred.astype(float)]
    actual_y = [y[0] for y in y_test.astype(float)]

    ridge_xy_df = pd.DataFrame({'x': predict_x,'y':actual_y,'model':'ridge_regression'})
    

    return ridge_xy_df


###########################################################
# calculate  model x and y  for lasso regression model
###########################################################
def lasso_xy_model(train_df):

    #convert train_df into model data
    model_data = train_df[["item_outlet_sales","item_MRP","item_fat_content","item_type","outlet_location_type","outlet_size","outlet_type"]]
    # One-hot Coding
    model_data = pd.get_dummies(model_data, columns = ["item_fat_content","item_type","outlet_location_type","outlet_size","outlet_type"])
    # float conversion
    model_data['item_outlet_sales'] = model_data['item_outlet_sales'].astype(float)

    #sklearn x & y tune-up
    Y = model_data["item_outlet_sales"].values
    X = model_data.drop("item_outlet_sales",axis = 1).values
    Y = Y.reshape(-1,1)
    # Split train and test data
    X_train,X_test,y_train,y_test = train_test_split(X,Y,test_size = 0.3,random_state = 42)

    # Lasso Regression
    lasso = Lasso(alpha=0.1,normalize=True)
    #names = model_data.drop("item_outlet_sales",axis = 1).columns
    lasso.fit(X_train,y_train)
    y_pred = lasso.predict(X_test)

    # Compute x and y into array
    predict_x = y_pred.astype(float)
    actual_y = [y[0] for y in y_test.astype(float)]

    lasso_xy_df = pd.DataFrame({'x': predict_x,'y':actual_y,'model':'lasso_regression'})
    

    return lasso_xy_df


########################################################################
# calculate  model x and y for non-regression model / decision tree
########################################################################
def dec_tree_xy_model(train_df):

    #convert train_df into model data
    model_data = train_df[["item_outlet_sales","item_visibility_mean_ratio","outlet_years","item_MRP","item_fat_content","item_type"
                            ,"outlet_location_type","outlet_size","outlet_type"]]

    # One-hot Coding
    model_data = pd.get_dummies(model_data, columns = ["item_fat_content","item_type","outlet_location_type","outlet_size","outlet_type"])
    # float conversion
    model_data['item_outlet_sales'] = model_data['item_outlet_sales'].astype(float)

    #sklearn x & y tune-up
    Y = model_data["item_outlet_sales"].values
    X = model_data.drop("item_outlet_sales",axis = 1).values
    Y = Y.reshape(-1,1)
    # Split train and test data
    X_train,X_test,y_train,y_test = train_test_split(X,Y,test_size = 0.3,random_state = 20)

    # decision tree
    regressor = DecisionTreeRegressor(random_state = 42,max_depth=10,min_samples_leaf=70)
    regressor.fit(X_train,y_train)
    y_pred = regressor.predict(X_test)

    # Compute x and y into array
    predict_x = y_pred.astype(float)
    actual_y = [y[0] for y in y_test.astype(float)]

    dec_tree_xy_df = pd.DataFrame({'x': predict_x,'y':actual_y,'model':'decision_tree'})
    

    return dec_tree_xy_df 


