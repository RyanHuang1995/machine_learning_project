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
#from sqlalchemy.pool import SingletonThreadPool


#pymysql.install_as_MySQLdb()

# model #1 linear regression
def linear_model(train_df):

    #convert train_df into model data
    model_data = train_df[["item_outlet_sales","item_MRP","item_fat_content","item_type","outlet_location_type","outlet_size","outlet_type"]]
    # One-hot Coding
    model_data = pd.get_dummies(model_data, columns = ["item_fat_content","item_type","outlet_location_type","outlet_size","outlet_type"])
    # float conversion
    model_data['item_outlet_sales'] = model_data['item_outlet_sales'].astype(float)

    #sklearn model
    Y = model_data["item_outlet_sales"].values
    X = model_data.drop("item_outlet_sales",axis = 1).values
    Y = Y.reshape(-1,1)
    # Split train and test data
    X_train,X_test,y_train,y_test = train_test_split(X,Y,test_size = 0.3,random_state = 42)
    reg_all = LinearRegression()
    reg_all.fit(X_train,y_train)
    y_pred = reg_all.predict(X_test)
    # Compute and print R^2 and RMSE
    rmse = np.sqrt(mean_squared_error(y_test,y_pred))
    r2 = format(reg_all.score(X_test, y_test))
    # 5-fold cross-validation
    reg = LinearRegression()
    cv_results = cross_val_score(reg,X,Y,cv = 5)
    # get x and y for residual plot
    predict_x = [x[0] for x in X_test.astype(float)]
    actual_y = [y[0] for y in y_test.astype(float)]

    #sklearn_model_stats = [{'R^2': r2, 'RMSE': rmse,'Cross-Validation Mean R^2': cv_results,'actual_y': actual_y, 'predict_x': predict_x}]
    sklearn_model_stats = [{'R^2': r2, 'RMSE': rmse,'Cross-Validation Mean R^2': cv_results}]

    return sklearn_model_stats





