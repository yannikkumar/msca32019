#!/bin/python3

import math
import os
import random
import re
import sys
import pandas as pd
import numpy as np

pd.set_option('display.max_rows', 10)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)


#
# Complete the 'case1' function below.
#
# The function accepts STRING_ARRAY fp_data as parameter.
#

def case1(financial_data):
    # Print First 5 rows of MSFT
    # Print Last 5 rows of MSFT
    # Print Describe MSFT
    print(financial_data.head())
    print(financial_data.tail())
    print(financial_data.describe())
    return None
    

def case2(financial_data):
    # Resample to monthly data
    # Display the first 5 rows
    monthly = financial_data.resample('M').mean()
    print(monthly.head(5))
    return None

def case3(financial_data):
    # Create a variable daily_close and copy Adj Close from financial_data
    # Print daily returns
    daily_close = financial_data['Adj Close']
    daily_returns = pd.DataFrame({'Adj Close': daily_close.pct_change()})
    print(daily_returns.iloc[1:, :])
    return None

def case4(financial_data):
    # Calculate the cumulative daily returns
    # Print it
    cum_daily_return = (1 + financial_data['Adj Close'].pct_change()).cumprod()
    cum_daily_return = pd.DataFrame({'Adj Close': cum_daily_return})
    print(cum_daily_return.iloc[1:, :])
    return None

def case5(financial_data):
    # Resample the cumulative daily return to cumulative monthly return
    cum_daily_return = (1 + financial_data['Adj Close'].pct_change()).cumprod()
    cum_monthly_return = cum_daily_return.resample("M").mean()
    cum_monthly_return = pd.DataFrame({'Adj Close': cum_monthly_return})
    print(cum_monthly_return)
    return None

def case6(financial_data):
    # Isolate the adjusted closing prices and store it in a variable
    # Calculate the moving average for a window of 20
    adj_close = financial_data['Adj Close']
    moving_avg = adj_close.rolling(window=20).mean()
    moving_avg = pd.DataFrame({'Adj Close': moving_avg})
    print(moving_avg)
    return None

def case7(financial_data):
    # Calculate the volatility for a period of 100 don't forget to multiply by square root
    # don't forget that you need to use pct_change
    returns = financial_data['Adj Close'].pct_change()
    volatility = returns.rolling(100).std()
    volatility = volatility * np.sqrt(100)
    volatility = pd.DataFrame({'Adj Close': volatility})
    print(volatility)
    return None   


def case8(financial_data):
    # Initialize the short rolling window (window=50)
    # Initialize the long rolling window (window=100)
    short_window = 50
    long_window = 100
    # You will create a signals dataframe
    # using the index of financial_data
    signals = pd.DataFrame(index=financial_data.index)
    # You will assign 0 to the column signal of the dataframe signals
    signals['signal'] = 0.0
    # Create short simple moving average over the short window
    signals['short_mavg'] = financial_data['Close'].rolling(window=short_window,
                                                                min_periods=1).mean()
    
    # Create long simple moving average over the long window
    signals['long_mavg'] = financial_data['Close'].rolling(window=long_window,
                                                               min_periods=1).mean()
    # You will not populate the value 1 when the small window moving average
    # is higher than the long window moving average else 0
    signals['signal'][short_window:] = np.where(signals['short_mavg'][short_window:]
                                                > signals['long_mavg'][short_window:], 
                                                1.0, 0.0)
    
    # Generate trading orders by inserting in a new column orders
    # 1 if it is a buy order -1 if it is a sell order
    # you should just use the diff command on the column signal
    signals['orders'] = signals['signal'].diff()
    
    # Print the dataframe signals
    print(signals)
    return None
    


def case9(financial_data):
    # You will need to use the dataframe signals
    short_window = 50
    long_window = 100
    signals = pd.DataFrame(index=financial_data.index)
    signals['signal'] = 0.0
    signals['short_mavg'] = financial_data['Close'].rolling(window=short_window,
                                                                min_periods=1).mean()
    signals['long_mavg'] = financial_data['Close'].rolling(window=long_window,
                                                               min_periods=1).mean()
    signals['signal'][short_window:] = np.where(signals['short_mavg'][short_window:]
                                                > signals['long_mavg'][short_window:], 
                                                1.0, 0.0)
    signals['orders'] = signals['signal'].diff()
    # You are going to set your initial amount of money you want
    # to invest --- here it is 10,000
    initial_money = 10000.0
    
    # You are going to create a new dataframe positions
    # Remember the index is still the same as signals
    positions = pd.DataFrame(index=signals.index).fillna(0.0)
    
    # You are going to buy 10 shares of MSFT when signal is 1
    # You are going to sell 10 shares of MSFT when signal is -1
    # You will assign these values to the column MSFT of the
    # dataframe positions
    positions['MSFT'] = 10 * signals['signal']
    
    # You are now going to calculate the notional (quantity x price)
    # for your portfolio. You will multiply Adj Close from
    # the dataframe containing prices and the positions (10 shares)
    # You will store it into the variable portfolio
    portfolio = positions.multiply(financial_data['Adj Close'], axis=0)
    
    # Add `holdings` to portfolio
    pos_diff = positions.diff()
    
    # You will store positions.diff into pos_diff
    portfolio['holdings'] = ((positions.multiply(financial_data['Adj Close'], axis=0))
                             .sum(axis=1))
    # You will now add a column cash in your dataframe portfolio
    # which will calculate the amount of cash you have
    # initial_capital - (the notional you use for your different buy/sell)
    portfolio['cash'] = initial_money - ((pos_diff.multiply(financial_data['Adj Close'], axis=0))
                                         .sum(axis=1).cumsum())
    
    # You will now add a column total to your portfolio calculating the part of holding
    # and the part of cash
    portfolio['total'] = portfolio['cash'] + portfolio['holdings']
    
    # Add `returns` to portfolio
    portfolio['returns'] = portfolio['total'].pct_change()
    
    # Print the first lines of `portfolio`
    print(portfolio)
    return None
    

if __name__ == '__main__':
    case_number=input().strip()
    df = pd.read_csv(sys.stdin, header=0, index_col='Date', parse_dates=True)
    globals()['case'+case_number](df)