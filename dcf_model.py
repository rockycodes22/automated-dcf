#Imports
import yfinance as yf
import pandas as pd

#------------------------
#GET FUNCTIONS
#------------------------

#  get revenues from a ticker

def get_income_statement(ticker):
    t_symbol = yf.Ticker(ticker)
    income_stmt = t_symbol.financials

    revenues = income_stmt.loc["Total Revenue"]
    clean_revenues = revenues.dropna()
    revenue_list = clean_revenues.to_list()
    revenue_list.reverse()

    ebits = income_stmt.loc["EBIT"]
    clean_ebits = ebits.dropna()
    ebit_list = clean_ebits.to_list()
    ebit_list.reverse()
   
    return revenue_list, ebit_list

   
# calculate ebit margin: ebit/revenue

def get_ebit_margins(revenues, ebits):
    ebit_margins = []

    for i in range(len(ebits)):
        temp_margin = ebits[i] / revenues[i]
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

#------------------------
#AVERAGE FUNCTIONS
#------------------------
          
# calculates the average growth rate
def average_growth(growth_rates):
     return sum(growth_rates)/len(growth_rates)

#calculates the average ebit margin
def average_ebit_margin(ebit_margins):
     return sum(ebit_margins)/len(ebit_margins)

#------------------------
#FORECAST FUNCTIONS
#------------------------

# forecasts the revenues
def forecast_revenues(last_revenue, growth_rate, forecast_years):
     forecasts = []
     revenue = last_revenue
     
     #loop that calculates forecasts
     for i in range(forecast_years):
          revenue = revenue * (1 + growth_rate)
          forecasts.append(revenue)
    
     return forecasts 


# forecasts the ebits
def forecast_ebits(forecasted_revenues, ebit_margin):
     forecasts = []

     #loop to calc ebits 
     for i in forecasted_revenues:
          temp_ebit = i * ebit_margin
          forecasts.append(temp_ebit)
    
     return forecasts 


# forecasts the NOPAT
def forecast_nopat(forecasted_ebits, tax_rate):
     forecasts = []

     #loop to calc NOPAT
     for i in forecasted_ebits:
          temp_nopat = i * (1-tax_rate)
          forecasts.append(temp_nopat)
     return forecasts 


# forecasts the D&A 
def forecast_da(forecasted_revenues, da_percentage):
     forecasts = []

     # loop to calc D&A
     for i in forecasted_revenues:
          temp_da = i * da_percentage
          forecasts.append(temp_da)
     return forecasts 


# forecasts the Capex
def forecast_capex(forecasted_revenues, capex_percentage):
     forecasts = []

     # loop to calc capex
     for i in forecasted_revenues:
          temp_capex = i * capex_percentage
          forecasts.append(temp_capex)
     return forecasts 


# forecasts the nwc
def forecast_nwc(forecasted_revenues, nwc_percentage):
     forecasts = []

     # loop to calc nwc
     for i in forecasted_revenues:
          temp_nwc = i * nwc_percentage
          forecasts.append(temp_nwc)
     return forecasts 

#------------------------
# UFCF
#------------------------

def forecast_ufcf(nopat, da, capex, nwc):
     forecasts = []
     
     #loop to calc ufcf
     for i in range(len(nopat)):
          temp_ufcf = nopat[i] + da[i] - capex[i] - nwc[i]
          forecasts.append(temp_ufcf)
     return forecasts


#discount ufcf
def discount_ufcf(ufcf, wacc):
     forecasts = []

     #loop to discount ufcf
     for i in range (len(ufcf)):
          temp_ufcf = ufcf[i]/(1+wacc)**(i+1)
          forecasts.append(temp_ufcf)
     return forecasts

#------------------------
#TERMINAL VALUE & EV
#------------------------

def find_terminal_value(ufcf, wacc, growth_rate):
     last_ufcf = ufcf[len(ufcf)-1]
     ufcf_n_plus_1 = last_ufcf * (1 + growth_rate)
     n = len(ufcf)

     tv = ufcf_n_plus_1/(wacc-growth_rate)
     pvtv = tv/(1+wacc)**n

     return pvtv

#calc EV
def find_ev(pv_ufcf, pv_tv):
     return pv_tv + sum(pv_ufcf)


#finds implied share price
def find_implied_share_price(ev,cash,debt,shares):
     net_debt = debt - cash
     equity_value = ev-net_debt
     return equity_value/shares

#------------------------
#SENSITIVITY TABLE
#------------------------

def sensitivity_table(ufcf,wacc_values,g_values):
     table = pd.DataFrame(index= wacc_values, columns = g_values)

     #nested for loop to calc
     for wacc in wacc_values:
         for g in g_values:
              pv_ufcf = discount_ufcf(ufcf, wacc)
              pv_tv = find_terminal_value(ufcf, wacc, g)
              ev = sum(pv_ufcf) + pv_tv
              table.loc[wacc, g] = ev
     
     return table


def run_dcf(ticker, assumptions):
    # pull data
      revenues, ebits = get_income_statement(ticker)
    # historical analysis

      ebit_margins = get_ebit_margins(revenues, ebits)
      growth_rates = get_growth_rates(revenues)

      avg_ebit_margin = average_ebit_margin(ebit_margins)
      avg_growth_rate = average_growth(growth_rates)

    # forecasting
      forecasted_revenues = forecast_revenues(revenues[-1],avg_growth_rate,assumptions["forecast_years"])
      forecasted_ebits = forecast_ebits(forecasted_revenues, avg_ebit_margin)

      forecasted_nopat = forecast_nopat(forecasted_ebits,assumptions["tax_rate"])
      forecasted_da = forecast_da(forecasted_revenues,assumptions["da_percentage"])
      forecasted_capex = forecast_capex(forecasted_revenues, assumptions["capex_percentage"])
      forecasted_nwc = forecast_nwc(forecasted_revenues, assumptions["nwc_percentage"])

      ufcf = forecast_ufcf(forecasted_nopat,forecasted_da, forecasted_capex, forecasted_nwc)
      pv_ufcf = discount_ufcf(ufcf,assumptions["wacc"])
      

    # valuation
      pv_tv = find_terminal_value(ufcf, assumptions["wacc"], assumptions["terminal_g"])
      ev = find_ev(pv_ufcf, pv_tv)
      implied_share_price = find_implied_share_price(ev, assumptions["cash"], assumptions["debt"], assumptions["shares_outstanding"])
    # sensitivity

      sensitivity = sensitivity_table(ufcf, assumptions["wacc_range"], assumptions["terminal_g_range"])

      results = {
      "summary": {
        "enterprise_value": ev,
        "implied_share_price": implied_share_price
      },
 
      "historical": {
        "revenues": revenues,
        "ebits": ebits,
        "ebit_margins": ebit_margins,
        "growth_rates": growth_rates
      },

      "forecast": {
        "revenues": forecasted_revenues,
        "ebits": forecasted_ebits,
        "nopat": forecasted_nopat,
        "ufcf": ufcf
      },

      "valuation": {
        "pv_ufcf": pv_ufcf,
        "pv_terminal_value": pv_tv,
        "sensitivity": sensitivity
      }
      }

      return results


