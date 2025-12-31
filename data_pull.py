#Imports
import yfinance as yf
import pandas as pd

#  get revenues from a ticker

def get_revenues(ticker):
    t_symbol = yf.Ticker(ticker)
    income_stmt = t_symbol.financials

    revenues = income_stmt.loc["Total Revenue"]
    clean_revenues = revenues.dropna()
    revenue_list = clean_revenues.to_list()
    revenue_list.reverse()

    return revenue_list


##get_revenues("AAPL")

# Gets the Ebits using a ticker symbol
def get_ebit(ticker):
     t_symbol = yf.Ticker(ticker)
     income_stmt = t_symbol.financials 

     ebits = income_stmt.loc["EBIT"]
     clean_ebits = ebits.dropna()
     ebit_list = clean_ebits.to_list()
     ebit_list.reverse()

     return ebit_list
   
# calculate ebit margin: ebit/revenue

def get_ebit_margin(ticker):
     ebit = get_ebit(ticker)
     revenue = get_revenues(ticker)

     ebit_margins = []

     # loop to calc ebit margins
     for i in range(len(ebit)):
          temp_margin = ebit[i]/revenue[i]
          ebit_margins.append(temp_margin)

     return ebit_margins



    

