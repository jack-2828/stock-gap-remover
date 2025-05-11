import yfinance as yf
import pandas as pd
from datetime import timedelta
import datetime
import os
current_date = datetime.datetime.today().strftime("%m-%d-%Y")
# incrementing the date by 1 day to ensure today's data is included
tomorrow_date = datetime.datetime.today() + timedelta(days=1)
tomorrow_date = tomorrow_date.strftime("%Y-%m-%d")

for num in range(3):
    if num == 0:
        dat_data = yf.Ticker('QQQ').history(period='1d', start='2024-01-01', end=tomorrow_date)
        name = "QQQ"
        dat_data.drop(columns=['Dividends', 'Stock Splits', "Capital Gains"], inplace=True)
        dat_data.index = pd.to_datetime(dat_data.index)
        dat_data.index = dat_data.index.strftime('%m-%d-%Y')
    else:
        if num == 1:
            dat1_data = yf.Ticker('XLY').history(period='1d', start='2020-01-01', end=tomorrow_date)
            dat2_data = yf.Ticker('XLP').history(period='1d', start='2020-01-01', end=tomorrow_date)
             # save these files to csv
            with open('XLY_raw_data.csv', 'w', newline='') as f:
                dat1_data.to_csv(f)
                f.close()
            with open('XLP_raw_data.csv', 'w', newline='') as f:
                dat2_data.to_csv(f)
                f.close()
            name = "XLY-vs-XLP"
        elif num == 2:
            dat1_data = yf.Ticker('RSPD').history(period='1d', start='2024-01-01', end=tomorrow_date)
            dat2_data = yf.Ticker('RSPS').history(period='1d', start='2024-01-01', end=tomorrow_date)
            name = "RSPD-vs-RSPS"
        dat1_data.drop(columns=['Dividends', 'Stock Splits', "Capital Gains"], inplace=True)
        dat1_data.index = pd.to_datetime(dat1_data.index)
        dat1_data.index = dat1_data.index.strftime('%m-%d-%Y')
        dat2_data.drop(columns=['Dividends', 'Stock Splits', "Capital Gains"], inplace=True)
        dat2_data.index = pd.to_datetime(dat2_data.index)
        dat2_data.index = dat2_data.index.strftime('%m-%d-%Y')
        ratio = pd.DataFrame()
        counter = 0
        for (index1, row1), (index2, row2) in zip(dat1_data.iterrows(), dat2_data.iterrows()):
            counter += 1
            if (index1 != index2):
                raise Exception("Stopping... dates in ratio don't match")
            new_ratio_row = pd.DataFrame({
                'Open':  [round(row1["Open"] / row2["Open"], 3)],
                'High':  [0],
                'Low':   [0],
                'Close': [round(row1['Close'] / row2["Close"], 3)]
            }, index=[index1])
            if counter < 10:
                print(counter)
                print(f'XLY / XLP : {index1} | {index2} {row1["Open"]} / {row2["Open"]}')

            ratio = pd.concat([ratio, new_ratio_row], axis=0)
        
        dat_data = ratio.copy(deep=True)
        with open(f'{name} ratio test.csv', 'w', newline="") as f:
            dat_data.to_csv(f)

    

    qqq_no_gaps = pd.DataFrame()
    qqq_no_gaps.index.name = 'Date'
    previous_close = 0
    for index, row in dat_data.iterrows():
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

    home = os.path.expanduser("~")
    desktop = os.path.join(home, "Desktop")
    target_folder = os.path.join(desktop, "StockCharts-User-Defined-Indexes")
    os.makedirs(target_folder, exist_ok=True)
    file_path = os.path.join(target_folder, f'{name}_no_gaps-{current_date}.csv')
    try: 
        # implement async file saving to speed up process
        with open(file_path, 'w', newline="") as f:
            qqq_no_gaps.to_csv(f, index_label="Date")
        print("File saved at", file_path)
    except:
        print("An error was encountered saving", file_path)