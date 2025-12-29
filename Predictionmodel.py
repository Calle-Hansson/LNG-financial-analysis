# -*- coding: utf-8 -*-
"""
Created on Sun Dec 21 15:09:14 2025

@author: calle

This file downloads the TTF (Dutch market price for natural gas priced in EUR/MWh)
and merges it witdh the exports dataset.
A number of lags are introuduced to account for the traveltime over the atlantic ocean.
finally a linear regression model is trained on the new dataset and asked to predict
the absolute change from one day to the next
"""

import pandas as pd
import yfinance as yf
from sklearn.linear_model import  LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error
import numpy as np


#%%

'''TTF is Downloaded from yfinance'''

TTF= yf.download(
    "TTF=F",
    start='2024-01-01',
    end='2024-12-31',
    progress=False
    )

TTF=TTF[['High']].copy()
if isinstance(TTF.columns,pd.MultiIndex):
    TTF.columns = TTF.columns.get_level_values(0)
    
TTF = TTF.reset_index()
TTF['Date'] = pd.to_datetime(TTF['Date']).dt.normalize()
TTF = TTF.rename(columns={"High":"TTF_High"})


#%%




df = pd.read_csv('LNG_Exports.csv', header=0, names= ['Date', 'Exports'])
df['Date']= pd.to_datetime(df['Date']).dt.normalize()

df.head()


df['7d']= df['Exports'].rolling(window=7).sum()
df['14d']= df['Exports'].rolling(window=14).sum()
df['21d']= df['Exports'].rolling(window=21).sum()

df = df.merge(TTF, on="Date", how= "left", ).set_index('Date')
df = df.dropna()


'''Here we save a csv file for use in the flask plotly graph'''
df.to_csv("LNG_Flask_app\Flask_Page\Flask_base_data.csv", index= True , header= True)



'''The different lags are created'''
df['TTF_Lag_1'] = df['TTF_High'].shift(1)
df['TTF_Lag_7'] = df['TTF_High'].shift(7)
df['TTF_Lag_14'] = df['TTF_High'].shift(14)
df['TTF_Lag_21'] = df['TTF_High'].shift(21)


df['TTF_Change'] = df['TTF_High'].diff()

#%%

'''The data is split between x,y and test and train.
the model is then asked to predict the y_pred based on the X_test
Mean Average Error (MAE) and Root Mean squared Error (RMSE) is then used to evaluate the predictionmodel. '''

model_df = df[['Exports','7d','14d','21d','TTF_Lag_1','TTF_Lag_7','TTF_Lag_14', 'TTF_Lag_21', 'TTF_Change'  ]].dropna()



X = model_df[['Exports','7d','14d','21d','TTF_Lag_1','TTF_Lag_7','TTF_Lag_14', 'TTF_Lag_21'  ]]
y = model_df['TTF_Change']



mask = X.notna().all(axis=1) & y.notna()
X = X[mask]
y = y[mask]


split= int(len(X)*0.8)

X_train, X_test = X.iloc[:split], X.iloc[split:]
y_train, y_test = y.iloc[:split], y.iloc[split:]


model = LinearRegression()


model.fit(X_train, y_train)

y_pred = model.predict(X_test)

mae_model = mean_absolute_error(y_test,y_pred)
rmse_model = np.sqrt(mean_squared_error(y_test,y_pred))

mae_zero = mean_absolute_error(y_test, np.zeros_like(y_test))
rmse_zero = np.sqrt(mean_squared_error(y_test,np.zeros_like(y_test)))

print(f"MAE Model {mae_model:.2f}, vs MAE Zero {mae_zero:.2f}")
print(f"RMSE Model {rmse_model:.2f}, vs RMSE Zero {rmse_zero:.2f}")


        
        
        
        
        


#%%






















