# -*- coding: utf-8 -*-
"""
Created on Fri Sep 23 21:55:48 2022

@author: sigma
"""

#This is from the CQF program where I want to modify. SO this is just work in progress.

# Import required libraries
import pandas as pd
from numpy import *
from scipy.stats import norm

import matplotlib.pyplot as plt
from tabulate import tabulate 

# Ignore warnings
import warnings
warnings.filterwarnings('ignore')




from BS import BS


# Initialize option
option = BS(100,100,0.02,0.12,0.22)

header = ['Option Price', 'Delta', 'Gamma', 'Theta', 'Vega', 'Rho']
table = [[option.callPrice, option.callDelta, option.gamma, option.callTheta, option.vega, option.callRho]]

print(tabulate(table,header))



#Visual
figure, axes = plt.subplots(1,2, figsize=(20,6), sharey=True)

x = linspace(50,150,100)
d = {'0M':1e-50, '3M': 0.25, '6M': 0.5, '9M': 0.75, '12M': 1.0}

for k,v in d.items():
    axes[0].plot(x, BS(x,100,0.0,v,0.2).callPrice, label=k)
    axes[1].plot(x, BS(x,100,0.0,v,0.2).putPrice, label=k)
    
# Set axis title
axes[0].set_title('Call Price'), axes[1].set_title('Put Price')

# Define legend
axes[0].legend(), axes[1].legend()

plt.show()


# Plot straddle price 
plt.plot(x, (BS(x,100,0.0,1,0.2).callPrice - BS(x,100,0.0,1,0.2).putPrice))
plt.title('ATM Straddle Price');

# Plot graph iteratively
fig, ax = plt.subplots(2,2, figsize=(20,10))

for k,v in d.items():
    ax[0,0].plot(x, BS(x,100,0.0,v,0.2).callDelta, label=k)
    ax[0,1].plot(x, BS(x,100,0.0,v,0.2).gamma, label=k)
    ax[1,0].plot(x, BS(x,100,0.0,v,0.2).vega, label=k)
    ax[1,1].plot(x, BS(x,100,0.0,v,0.2).callTheta, label=k)
    
# Set axis title
ax[0,0].set_title('Delta'), ax[0,1].set_title('Gamma'), ax[1,0].set_title('Vega'), ax[1,1].set_title('Theta')

# Define legend
ax[0,0].legend(), ax[0,1].legend(), ax[1,0].legend(), ax[1,1].legend()

plt.show()

#Use yahoo finance data
import yfinance as yf

# Get SPY option chain
spy = yf.Ticker('SPY')
options =  spy.option_chain('2021-03-31')


# March 2021 335 SPY call option price
spot = 335
strike = 335
rate = 0.0
dte = 0.3945
vol = 0.2185
spy_opt = BS(spot,335,rate,dte,vol)

print(f'Option Price of SPY201231C00335000 with BS Model is {spy_opt.callPrice:0.4f}')

# Filter calls for strike above 330
df = options.calls[options.calls['strike']>330]
df.reset_index(drop=True, inplace=True)

# Check the filtered output
df.iloc[:,:11].head()

# Dataframe manipulation with selected fields
df = pd.DataFrame({'Strike': df['strike'], 
                   'Price': df['lastPrice'], 
                   'ImpVol': df['impliedVolatility']})
# Check output
df.head(2)

# Derive greeks and assign to dataframe as columns
df['Delta'] = df['Gamma'] = df['Vega'] = df['Theta'] = 0.

for i in range(len(df)):
    
    df['Delta'].iloc[i] = BS(spot,df['Strike'].iloc[i],rate,dte,df['ImpVol'].iloc[i]).callDelta
    df['Gamma'].iloc[i] = BS(spot,df['Strike'].iloc[i],rate,dte,df['ImpVol'].iloc[i]).gamma
    df['Vega'].iloc[i] = BS(spot,df['Strike'].iloc[i],rate,dte,df['ImpVol'].iloc[i]).vega
    df['Theta'].iloc[i] = BS(spot,df['Strike'].iloc[i],rate,dte,df['ImpVol'].iloc[i]).callTheta
    
# Verify output
df.head()

# Verify output
df.head()