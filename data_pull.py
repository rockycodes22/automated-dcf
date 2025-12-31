#Imports
import yfinance as yf
import pandas as pd

#Function to get revenues from a ticker

def get_revenues(ticker):
    t_symbol = yf.Ticker(ticker)
    income_stmt = t_symbol.financials

    revenues = income_stmt.loc["Total Revenue"]
    clean_revenues = revenues.dropna()
    revenue_list = clean_revenues.to_list()
    revenue_list.reverse()




    

