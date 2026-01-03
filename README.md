# Automated DCF Valuation Model (Python + Excel)

## Overview
This project is a fully automated **Discounted Cash Flow (DCF) valuation model** built in Python, designed to mirror how DCFs are constructed and analyzed in **investment banking and private equity**.

The model intentionally separates responsibilities:
- **Excel** → input and presentation layer  
- **Python** → calculation and automation engine  

By changing only the ticker and assumptions in Excel and re-running the script, the entire valuation recalculates deterministically.

---

## Key Features
- Pulls historical financials by ticker using `yfinance`
- Cleans and processes revenues and EBIT
- Computes historical growth rates and margins
- Forecasts:
  - Revenues
  - EBIT
  - NOPAT
  - D&A, CapEx, and ΔNWC
  - Unlevered Free Cash Flow (UFCF)
- Discounts cash flows using WACC
- Computes terminal value using the Gordon Growth method
- Calculates Enterprise Value and implied share price
- Builds a **WACC × terminal growth sensitivity table**
- Exports clean, formatted outputs back into Excel:
  - Summary valuation
  - Sensitivity table with conditional formatting

---


## File Descriptions

### `dcf_model.py`
Contains all valuation logic, including:
- Data extraction and cleaning
- Forecasting functions
- UFCF construction
- Discounting and terminal value calculation
- Sensitivity analysis
- `run_dcf(ticker, assumptions)` orchestrator that runs the full model end-to-end

This file is intentionally kept modular and readable, similar to an Excel-based financial model.

---

### `run_from_excel.py`
Acts as the execution layer between Excel and Python:
- Reads the ticker and assumptions from `dcf_inputs.xlsx`
- Builds the assumptions dictionary
- Calls `run_dcf()`
- Writes outputs back into Excel:
  - Summary valuation
  - Sensitivity table
- Applies Excel formatting (currency, column widths, conditional formatting)

Excel does not perform calculations — it only provides inputs and displays outputs.

---

### `dcf_inputs.xlsx`
Serves as both:
- **Input sheet** — ticker, WACC, growth rates, operating assumptions
- **Output sheets** — valuation summary and sensitivity analysis

This design keeps the model auditable and easy to use.

---

## How to Run the Model

### 1. Install dependencies
```bash
pip install pandas yfinance openpyxl

### 2. Update inputs in Excel
Open `dcf_inputs.xlsx` and modify:
- Ticker
- Valuation assumptions
- Operating assumptions
- Sensitivity ranges

Save the file.

python run_from_excel.py

### 3. View results
Open `dcf_inputs.xlsx` to see:
- Updated Enterprise Value and implied share price
- WACC × terminal growth sensitivity table

## Future Improvements
This project is still a work in progress. Planned extensions include:
- Excel button execution using `xlwings`
- Additional forecast output tables
- Scenario and case analysis
- Improved validation and error handling