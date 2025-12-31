
import pandas as pd

# ASSUMPTIONS
wacc = 0.10
terminal_growth = 0.03


# OPERATING FORECAST (SAMPLE DATA)

# Revenue forecast (base year + 5 years)
revenues = [100, 105, 110.25, 115.76, 121.55, 127.63]

# EBIT margin
ebit_margin = 0.20

# Tax rate
tax_rate = 0.25

# D&A, CapEx, ΔNWC assumptions
da = [3.0, 3.1, 3.2, 3.3, 3.4, 3.5]
capex = [5.0, 5.2, 5.4, 5.6, 5.8, 6.0]
delta_nwc = [1.0, 1.1, 1.2, 1.3, 1.4, 1.5]


# EBIT

ebit = []

for r in revenues:
    ebit_value = r * ebit_margin
    ebit.append(ebit_value)

# NOPAT

nopat = []

for e in ebit:
    nopat_value = e * (1 - tax_rate)
    nopat.append(nopat_value)


# UNLEVERED FREE CASH FLOW (UFCF)

ufcf = []

for i in range(len(nopat)):
    ufcf_value = nopat[i] + da[i] - capex[i] - delta_nwc[i]
    ufcf.append(ufcf_value)

# DISCOUNT UFCF

pv_ufcf = []

for i in range(1, len(ufcf)):
    pv_value = ufcf[i] / (1 + wacc) ** i
    pv_ufcf.append(pv_value)


# TERMINAL VALUE

final_ufcf = ufcf[-1]
terminal_value = (final_ufcf * (1 + terminal_growth)) / (wacc - terminal_growth)

n = len(ufcf) - 1
pv_terminal_value = terminal_value / (1 + wacc) ** n


# ENTERPRISE VALUE

enterprise_value = sum(pv_ufcf) + pv_terminal_value


# EQUITY VALUE & SHARE PRICE

total_debt = 40.0
cash = 20.0
shares_outstanding = 6.0

net_debt = total_debt - cash
equity_value = enterprise_value - net_debt
implied_share_price = equity_value / shares_outstanding


# OUTPUT

print("Enterprise Value:", round(enterprise_value, 2))
print("Equity Value:", round(equity_value, 2))
print("Implied Share Price:", round(implied_share_price, 2))

# RESULTS
results = {
    "Metric": [
        "Enterprise Value",
        "Equity Value",
        "Implied Share Price"
    ],
    "Value": [
        round(enterprise_value, 2),
        round(equity_value, 2),
        round(implied_share_price, 2)
    ]
}
# EXCEL
df = pd.DataFrame(results)

df.to_excel("DCF_Output.xlsx", index=False)