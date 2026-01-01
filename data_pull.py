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

# function to calculate historical growth rates
def get_growth_rates(revenues):
     growth_rates = []

     #loop to calc rates
     for i in range(1,len(revenues)):
          temp_rate = revenues[i]/revenues[i-1] - 1
          growth_rates.append(temp_rate)
     
     return growth_rates
          
#revenues = get_revenues("AAPL")
#growth_rates = get_growth_rates(revenues)
          
# calculates the average growth rate
def average_growth(growth_rates):
     return sum(growth_rates)/len(growth_rates)

# forecasts the revenues
def forecast_revenues(last_revenue, growth_rate, forecast_years):
     forecasts = []
     revenue = last_revenue
     
     #loop that calculates forecasts
     for i in range(forecast_years):
          revenue = revenue * (1 + growth_rate)
          forecasts.append(revenue)
     return forecasts 

print(forecast_revenues(100, 0.05, 3))