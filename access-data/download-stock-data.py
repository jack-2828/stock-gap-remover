import yfinance as yf
import pandas as pd
import datetime
dat = yf.Ticker('QQQ')
# QQQ 1-1-2024 - 10-1-2025
qqq_data = dat.history(period='1d', start='2024-01-01', end='2025-10-01')
print(qqq_data.columns)
qqq_data.drop(columns=['Dividends', 'Stock Splits', "Capital Gains"], inplace=True)
qqq_data.index = pd.to_datetime(qqq_data.index)
qqq_data.index = qqq_data.index.strftime('%m-%d-%Y')
qqq_no_gaps = pd.DataFrame()
qqq_no_gaps.index.name = 'Date'
previous_close = 0
for index, row in qqq_data.iterrows():
    aligned_prev_close = qqq_data["Close"].shift(1)
    if previous_close == 0:
        new_row = pd.DataFrame({
            'Open':  [round(row['Open'], 2)],
            'High':  [0],
            'Low':   [0],
            'Close': [round(row['Close'], 2)]
        }, index=[index])
    else: 
        adj_open = round(previous_close, 2)
        adj_close = round((row['Close'] - row['Open']) + adj_open, 2)
        new_row = pd.DataFrame({'Open': [adj_open], 'High': [0], 'Low': [0], 'Close': [adj_close]}, index=[index])
    qqq_no_gaps = pd.concat([qqq_no_gaps, new_row], axis=0)
    previous_close = row['Close']


print(qqq_no_gaps)

with open('./data/QQQ_no_gaps.csv', 'w') as f:
    qqq_no_gaps.to_csv(f, index_label="Date")