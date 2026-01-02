#imports
import pandas as pd
from dcf_model import run_dcf

#pandas dataframe
df = pd.read_excel("dcf_inputs.xlsx", sheet_name="inputs", header=None)
df.columns = ["label", "value"]



ticker = df.loc[df["label"] == "Ticker", "value"].values[0]


#assumptions 
assumptions = {
    "wacc": df.loc[df["label"] == "WACC", "value"].values[0],
    "terminal_g": df.loc[df["label"] == "Terminal Growth", "value"].values[0],
    "tax_rate": df.loc[df["label"] == "Tax Rate", "value"].values[0],
    "forecast_years": int(df.loc[df["label"] == "Forecast Years", "value"].values[0]),
    "da_percentage": df.loc[df["label"] == "D&A %", "value"].values[0],
    "capex_percentage": df.loc[df["label"] == "CapEx %", "value"].values[0],
    "nwc_percentage": df.loc[df["label"] == "NWC %", "value"].values[0],
    "cash": df.loc[df["label"] == "Cash", "value"].values[0],
    "debt": df.loc[df["label"] == "Debt", "value"].values[0],
    "shares_outstanding": df.loc[df["label"] == "Shares Outstanding", "value"].values[0], 
    "wacc_range": [float(x) for x in df.loc[df["label"] == "WACC Range", "value"].values[0].split(",")],
    "terminal_g_range": [float(x) for x in df.loc[df["label"] == "Terminal g Range", "value"].values[0].split(",")],
}

results = run_dcf(ticker, assumptions)
print(results["summary"])
