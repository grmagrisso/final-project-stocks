"""""
Name: Grace Magrisso
Assignment: Final Project
Section Leader: Kapua Ioane
Module Summary: This module is my ISTA 131 Final Project. I worked on this project independently. I used two datasets from Kaggle.com: "google_stock_price.csv" and "AAPL.csv".
These datasets contain data for these companies' opening and closing stock prices over several years. I will examin the opening and closing prices during January 2020.
I define six functions that work to produce three plots, two of which are scatter plots with linear regression lines, and the third is a bar chart.
The first two figures showcase the opening vs closing prices of Google and Apple respectively. The third figure compares the % change rate of Google and Apple's daily opening and closing stock prices via a bar plot.
"""""

# import modules
from turtle import color, pos, position, setposition
from distutils.command import clean
from functools import partial
from multiprocessing import Value
from pickle import FALSE
from tkinter import font
from xml.sax import default_parser_list
import numpy as np
from datetime import date, datetime
import csv
import pandas as pd
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import statsmodels.api as sm
import pytz as py

def filter_google():
    """
    Purpose: This function cleans the csv file "google_stock_price.csv" that contains stock data of Google's financial history.
    Return: a pandas Dataframe that has dates as indices and columns that contain opening $, closing $, and daily % change of opening and closing stock prices
    """
    # load in csv file with Google stock data
    file = pd.read_csv("google_stock_price.csv")

    # reformat date strings to datetime objects
    file["Date"] = pd.to_datetime(file["Date"], format = "%Y-%m-%d")

    # filter Jan 2020 data, scope = one month
    clean = file[file.Date >= datetime(2020, 1, 1)]
    clean_data = clean[clean.Date < datetime(2020, 2, 1)]

    # series of date count and timestamps
    january_dates = clean_data.iloc[:,0]

    # make date dataframe and make list of dates to set as indices
    df_dates = pd.DataFrame(january_dates)
    date_list = []
    for row in df_dates.index:
         for col in df_dates.columns:
              date_list.append((df_dates.loc[row,col]))

    # make series of date count and prices
    closing_prices = clean_data.iloc[:,4]
    opening_prices = clean_data.iloc[:,1]

    # make dataframe with timestamps as indices and opening and closing prices as columns
    df = pd.concat([opening_prices, closing_prices], axis = 1)
    df.index = date_list

    # add 3rd column for daily price change
    percent_change = []
    for i in range(len(df.index)):
         change = (df.Close[i] - df.Open[i]) / df.Open[i] * 100
         percent_change.append(change.round(2))
    df["Daily % Change"] = percent_change
    
    return df

def google_scatter_plot(df):
    """
    # Assisted by Rich Thompson
    Purpose: This function defines a scatter plot of Google's opening by closing stock prices during the month of January in 2020. Displays a linear regression line.
    Variable: df, a pandas Dataframe
    Returns: None
    """
    # define series with x and y values as opening and closing prices:
    f1 = plt.figure(1, figsize= (14,8))
    x = df.Open.values

    # y,x when plots
    s = pd.Series(df.Close.values,x)
    
    # scatter plot of opening vs closing prices with linear regression line:
    s.plot(linestyle = "", marker = "o", markersize = 9, color = "navy")
    X = sm.add_constant(x)
    model = sm.OLS(s,X)
    results = model.fit()
    y = results.params.loc["x1"] * x + results.params.loc["const"]
    
    # ticks
    my_xticks = []
    for i in range(67, 75, 1):
        my_xticks.append(i)
        my_xticks.append(i + 0.5)

    my_yticks = []
    for i in range(68,75,1):
        my_yticks.append(i)
        my_yticks.append(i + 0.5)

    # plot and add design features:
    plt.plot(x, y, linewidth = 3, color = "orangered")
    plt.title("Google's Daily Opening and Closing Stock Prices during January of 2020", fontsize = "medium", fontweight = "bold", color = "navy", size = 20)
    plt.xlabel("Opening share prices in USD", fontweight = "bold", color = "navy", size = 15)
    plt.ylabel("Closing share prices in USD", fontweight = "bold", color = "navy", size = 15)
    plt.grid(color = "slategrey")
    plt.gcf().set_facecolor("azure")
    plt.xticks(my_xticks, rotation = 45)
    plt.yticks(my_yticks)

def filter_apple():
    """
    Purpose: This function cleans the csv file "AAPL.csv" that contains stock data of Apple's financial history.
    Return: a pandas Dataframe that has dates as indices and columns that contain opening $, closing $, and daily % change of opening and closing stock prices
    """
    # load in csv file with Apple stock data
    file = pd.read_csv("AAPL.csv", parse_dates=["date"])

    # change dates to datetime objects
    clean_dates = []
    for stamp in range(len(file.date)):
        d = file.date[stamp]
        d = d.to_pydatetime()
        clean_dates.append(d)
    file.date = clean_dates
    df = file[['open', 'close']]
    df.index = clean_dates

    # filter data to only account for the month of Jan 2020
    jan_dates = []
    for row in range(len(df.index)):
        dic = df.index[row]
        if dic.month == 1 and dic.year == 2020:
            jan_dates.append(dic)
    
    opening_prices = []
    closing_prices = []
    for date in jan_dates:
        open = df.loc[date, "open"]
        opening_prices.append(open)
        close = df.loc[date, "close"]
        closing_prices.append(close)

    # create pandas dataframe with dates (dt) as index and three columns: open $, close $, and % change
    cleaned_jan_df = pd.DataFrame(index = jan_dates)
    cleaned_jan_df["Open"] = opening_prices
    cleaned_jan_df["Close"] = closing_prices
    cleaned_jan_df["Daily % Change"] = "x"
    
    # calculate and add in percent change column
    percent_change = []
    for i in range(len(cleaned_jan_df.index)):
         change = (cleaned_jan_df.Close[i] - cleaned_jan_df.Open[i]) / cleaned_jan_df.Open[i] * 100
         percent_change.append(change.round(2))
    cleaned_jan_df["Daily % Change"] = percent_change

    return cleaned_jan_df

def apple_scatter_plot(df):
    """
    Purpose: This function defines a scatter plot of Apple's opening by closing stock prices during the month of January in 2020. Displays a linear regression line.
    Variable: df, a pandas Dataframe
    Returns: None
    """
    f2 = plt.figure(2, figsize= (14,8))
    x = df.Open.values

    # y,x when plots
    s = pd.Series(df.Close.values,x)

    # scatter plot of opening vs closing prices with linear regression line:
    s.plot(linestyle = "", marker = "o", markersize = 9, color = "navy")
    X = sm.add_constant(x)
    model = sm.OLS(s,X)
    results = model.fit()
    y = results.params.loc["x1"] * x + results.params.loc["const"]

    my_xticks = []
    for i in range(293,325,1):
        my_xticks.append(i)

    my_yticks = []
    for i in range(297,325,1):
        my_yticks.append(i)

    # plot and add design features:
    plt.plot(x, y, linewidth = 3, color = "orangered")
    plt.title("Apple's Daily Opening and Closing Stock Prices during January of 2020", fontsize = "medium", fontweight = "bold", color = "navy", size = 20)
    plt.xlabel("Opening share prices in USD", fontweight = "bold", color = "navy", size = 15)
    plt.ylabel("Closing share prices in USD", fontweight = "bold", color = "navy", size = 15)
    plt.grid()
    plt.gcf().set_facecolor("azure")
    plt.xticks(my_xticks, rotation = 45)
    plt.yticks(my_yticks)
    
def open_close_change(dfa, dfg):
    """
    Purpose: This function defines a bar plot that displays the % change in Apple and Google's daily stock prices 1/2020
    Variables: dfa, a pandas Dataframe that contains data of Apple's stocks opening and closing prices and daily % change.
    dfg, a pandas Dataframe that contains data of Google's stocks opening and closing prices and daily % change.
    Returns: None
    """
    # convert indices in datetime64 to strings
    si = dfg.index.values
    day = []
    for i in si:
        string = str(i)
        string = string[8:10]
        day.append(string)
    indices = []
    for value in day:
         complete_date = "1-" + value
         indices.append(complete_date)

    # make new dataframe with % change values of both data frames as columns and dates as indices
    apple_per = []
    for percent in dfa["Daily % Change"]:
         apple_per.append(float(percent))
    google_per = []
    for percent in dfg["Daily % Change"]:
        google_per.append(float(percent))
    df_plot = pd.DataFrame(index = indices)

    # define company columns
    df_plot["Apple"] = apple_per
    df_plot["Google"] = google_per

    # create plot
    df_plot.plot(kind = "bar", figsize = (14,8), color = ["navy","orangered"])
    plt.xticks(rotation = 45)
    plt.title("Apple and Google's Daily Stock $ Change", fontweight = "bold", color = "navy", size = 20)
    # no vertical grid lines
    plt.grid(axis= "y", color = "slategrey")
    plt.gcf().set_facecolor("azure")
    plt.xlabel("Date (2020)", fontweight = "bold", color = "navy", size = 13)
    plt.ylabel("Daily % change of opening and closing stock prices", fontweight = "bold", color = "navy", size = 13)
    # add more ticks of y axis
    my_yticks = [-3.75, -3.5, -3.25, -3, -2.75, -2.5, -2.25, -2, -1.75, -1.5, -1.25, -1, -0.75, -0.5, -0.25, 0, 0.25, 0.5, 0.75, 1, 1.25, 1.5, 1.75, 2, 2.25, 2.5, 2.75, 3, 3.25, 3.5]
    plt.yticks(my_yticks)

def main():
    """
    Purpose: Calls the five functions above to create dataframes of Google and Apple's opening, closing, and daily % change of its stock prices during 1/20.
    Then, main displays three graphs and prints the dataframes.
    Parameter: None
    Return Value: None
    """
    a_df = filter_apple()
    g_df = filter_google()

    # figure 1 - Google Scatter
    google_scatter_plot(g_df)

    # figure 2 - Apple Scatter
    apple_scatter_plot(a_df)

    # figure 3 - Bar plot
    open_close_change(g_df, a_df)

    print()
    print("Google's January 2020 Stock Prices")
    print(g_df)
    print()
    print("Apple's January 2020 Stock Prices")
    print(a_df)
    plt.show()

if __name__ == "__main__":
	main()