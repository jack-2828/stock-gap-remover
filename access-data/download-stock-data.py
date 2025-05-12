import yfinance as yf
import pandas as pd
from datetime import timedelta
import datetime
import os
import asyncio


class GenerateData():
    def __init__(self):
        self.current_date = datetime.datetime.today().strftime("%m-%d-%Y")
        # incrementing the date by 1 day to ensure today's data is included
        self.tomorrow_date = datetime.datetime.today() + timedelta(days=1)
        self.tomorrow_date = self.tomorrow_date.strftime("%Y-%m-%d")
    def create_no_gap(self):
        for num in range(3):
            if num == 0:
                dat_data = self.get_stock_data("QQQ")
                self.name = "QQQ"
            else:
                if num == 1:
                    dat1_data = self.get_stock_data('XLY')
                    dat2_data = self.get_stock_data('XLP')
                    self.name = "XLY-vs-XLP"
                elif num == 2:
                    dat1_data = self.get_stock_data('RSPD')
                    dat2_data = self.get_stock_data('RSPS')
                    self.name = "RSPD-vs-RSPS"
                ratio = pd.DataFrame()
                for (index1, row1), (index2, row2) in zip(dat1_data.iterrows(), dat2_data.iterrows()):
                    if (index1 != index2):
                        raise Exception("Stopping... dates in ratio don't match")
                    new_ratio_row = pd.DataFrame({
                        'Open':  [round(row1["Open"] / row2["Open"], 4)],
                        'High':  [0],
                        'Low':   [0],
                        'Close': [round(row1['Close'] / row2["Close"], 4)]
                    }, index=[index1])
                    ratio = pd.concat([ratio, new_ratio_row], axis=0)
                
                dat_data = ratio.copy(deep=True)
            no_gaps_data = pd.DataFrame()
            # no_gaps_data.index.name = 'Date'
            previous_close = 0
            for index, row in dat_data.iterrows():
                if previous_close == 0:
                    new_row = pd.DataFrame({
                        'Open':  [round(row['Open'], 4)],
                        'High':  [0],
                        'Low':   [0],
                        'Close': [round(row['Close'], 4)]
                    }, index=[index])
                    previous_close = row['Close']
                else:
                    adj_open = round(previous_close, 4)
                    adj_close = round((row['Close'] - row['Open']) + adj_open, 4)
                    new_row = pd.DataFrame({
                        'Open': [adj_open],
                        'High': [0],
                        'Low': [0],
                        'Close': [adj_close]
                        }, index=[index])
                    previous_close = adj_close
                no_gaps_data = pd.concat([no_gaps_data, new_row], axis=0)
            self.save_data(no_gaps_data)
    def get_stock_data(self, ticker: str) -> pd.DataFrame:
        dat_data = yf.Ticker(ticker).history(period='1d', start='2024-01-01', end=self.tomorrow_date)
        dat_data.drop(columns=['Dividends', 'Stock Splits', "Capital Gains"], inplace=True)
        dat_data.index = pd.to_datetime(dat_data.index)
        dat_data.index = dat_data.index.strftime('%m-%d-%Y')
        return dat_data
    def save_data(self, df: pd.DataFrame):
        '''
        Save the given no-gap pandas dataframe to disk as a .csv

        df: The data-frame to be saved as a .csv
        '''
        home = os.path.expanduser("~")
        desktop = os.path.join(home, "Desktop")
        target_folder = os.path.join(desktop, "StockCharts-User-Defined-Indexes")
        os.makedirs(target_folder, exist_ok=True)
        file_path = os.path.join(target_folder, f'{self.name}_no_gaps-{self.current_date}.csv')
        try: 
            # implement async file saving to speed up process
            with open(file_path, 'w', newline="") as f:
                df.to_csv(f, index_label="Date")
            print("File saved at", file_path)
        except:
            print("An error was encountered saving", file_path)

if __name__ == "__main__":
    get_data = GenerateData()
    get_data.create_no_gap()