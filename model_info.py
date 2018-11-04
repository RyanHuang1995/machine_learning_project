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
# calculate model R^2 and RMSE for linear regression model
###########################################################
def sklearn_model(train_df):

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
    # Compute and print R^2 and RMSE
    sklearn_rmse = np.sqrt(mean_squared_error(y_test,y_pred))
    sklearn_r2 = format(reg_all.score(X_test, y_test))
    
    sklearn_model_df = pd.DataFrame({'model':'linear_regression','r2': sklearn_r2, 'RMSE': sklearn_rmse},index=[0])

    return sklearn_model_df

###########################################################
# calculate model R^2 and RMSE for ridge regression model
###########################################################
def ridge_model(train_df):

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

    # Compute and print R^2 and RMSE
    ridge_r2 = format(ridge.score(X_test, y_test))
    ridge_rmse = np.sqrt(mean_squared_error(y_test,y_pred))

    ridge_model_df = pd.DataFrame({'model':'ridge_regression','r2':ridge_r2, 'RMSE': ridge_rmse},index=[0])
    

    return ridge_model_df


###########################################################
# calculate model R^2 and RMSE for lasso regression model
###########################################################
def lasso_model(train_df):

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
    names = model_data.drop("item_outlet_sales",axis = 1).columns
    lasso.fit(X_train,y_train)
    y_pred = lasso.predict(X_test)

    # Compute and print R^2 and RMSE
    lasso_r2 = format(lasso.score(X_test, y_test))
    lasso_rmse = np.sqrt(mean_squared_error(y_test,y_pred))

    lasso_model_df = pd.DataFrame({'model':'lasso_regression','r2':lasso_r2, 'RMSE': lasso_rmse},index=[0])
    

    return lasso_model_df


########################################################################
# calculate model R^2 and RMSE for non-regression model / decision tree
########################################################################
def dec_tree_model(train_df):

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

    # Compute and print R^2 and RMSE
    dec_tree_rmse = format(np.sqrt(mean_squared_error(y_test,y_pred)))
    dec_tree_r2 = 'n/a'

    decission_tree_df = pd.DataFrame({'model':'decission_tree','r2':dec_tree_r2, 'RMSE': dec_tree_rmse },index=[0])
    

    return decission_tree_df


########################################################################
# use decision tree model to predict sales
########################################################################
def dec_tree_prediction(train_df,test_df):

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

    #start prediction
    predict_data = test_df[["item_visibility_mean_ratio","outlet_years","item_MRP","item_fat_content","item_type","outlet_location_type","outlet_size","outlet_type"]]
    predict_data = pd.get_dummies(predict_data, columns = ["item_fat_content","item_type","outlet_location_type","outlet_size","outlet_type"])
    X = predict_data.values
    predict_data["item_sales"] = regressor.predict(X)
   

    return predict_data



