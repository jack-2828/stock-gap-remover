import yfinance as yf
import pandas as pd
from datetime import timedelta
import datetime

dat = yf.Ticker('QQQ')
current_date = datetime.datetime.today().strftime("%m-%d-%Y")
# incrementing the date by 1 day to ensure today's data is included
tomorrow_date = datetime.datetime.today() + timedelta(days=1)
tomorrow_date = tomorrow_date.strftime("%Y-%m-%d")

qqq_data = dat.history(period='1d', start='2024-01-01', end=tomorrow_date)
qqq_data.drop(columns=['Dividends', 'Stock Splits', "Capital Gains"], inplace=True)
qqq_data.index = pd.to_datetime(qqq_data.index)
qqq_data.index = qqq_data.index.strftime('%m-%d-%Y')

qqq_no_gaps = pd.DataFrame()
qqq_no_gaps.index.name = 'Date'
previous_close = 0
for index, row in qqq_data.iterrows():
    if previous_close == 0:
        new_row = pd.DataFrame({
            'Open':  [round(row['Open'], 2)],
            'High':  [0],
            'Low':   [0],
            'Close': [round(row['Close'], 2)]
        }, index=[index])
        previous_close = row['Close']
    else:
        adj_open = round(previous_close, 2)
        adj_close = round((row['Close'] - row['Open']) + adj_open, 2)
        new_row = pd.DataFrame({
            'Open': [adj_open],
            'High': [0],
            'Low': [0],
            'Close': [adj_close]
            }, index=[index])
        previous_close = adj_close
    qqq_no_gaps = pd.concat([qqq_no_gaps, new_row], axis=0)

with open(f'./data/QQQ_no_gaps-{current_date}.csv', 'w') as f:
    qqq_no_gaps.to_csv(f, index_label="Date")