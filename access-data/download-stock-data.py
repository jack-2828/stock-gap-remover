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
previous_close = 0
for index, row in qqq_data.iterrows():
    if previous_close == 0:
        previous_close = row['Close']
        qqq_no_gaps = qqq_no_gaps.add(row)
    # else: 
        # daily_change = row['Close'] - row['Open']
        # previous_close = row['Close']
        # qqq_no_gaps = qqq_no_gaps.append(row)
print(qqq_no_gaps)
with open('./data/QQQ_no_gaps.csv', 'w') as f:
    qqq_data.to_csv(f)
    f.write('\n')
    f.write('Date,Open,High,Low,Close,Volume,Dividends,Stock Splits\n')

