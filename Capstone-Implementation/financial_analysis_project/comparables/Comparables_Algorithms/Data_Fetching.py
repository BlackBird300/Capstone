import yfinance as yf
import pandas as pd
import warnings
from datetime import datetime
import logging
import numpy as np

warnings.filterwarnings('ignore')
logging.basicConfig(level=logging.INFO)

class Data_Fetching:

    def __init__(self):
        self.data_DTW = None
        self.data_Clustering = None

    def Prepare_Data_DTW(self):

        url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
        tables = pd.read_html(url)
        sp500_table = tables[0]
        sp500_companies = sp500_table[['Symbol', 'Security', 'GICS Sector']]
        sp500_companies.columns = ['Symbol', 'Name', 'Sector']

        end_date = pd.Timestamp.today()
        start_date = end_date - pd.DateOffset(years=3)
        symbols = sp500_companies['Symbol'].tolist()
        data = yf.download(symbols, start=start_date, end=end_date, group_by='column', threads=True)
        data.columns.names = ['Field', 'Symbol']
        data = data.swaplevel(axis=1)
        data = data.stack(level='Symbol').reset_index()
        data = data.merge(sp500_companies, on='Symbol', how='left')
        data = data[['Date', 'Symbol', 'Name', 'Sector', 'Adj Close', 'Close', 'High', 'Low', 'Open', 'Volume']]
        # turn these features into numeric
        numeric_features = ['Adj Close', 'Close', 'High', 'Low', 'Open', 'Volume']
        data[numeric_features] = data[numeric_features].apply(pd.to_numeric, errors='coerce')
        # fill missing values with the mean of the sector
        data[numeric_features] = data.groupby('Sector')[numeric_features].transform(lambda x: x.fillna(x.mean()))
        self.data_DTW =data.copy()

        return self.data_DTW

    def Prepare_Data_Clustering(self):
            
            url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
            tables = pd.read_html(url)
            sp500_table = tables[0]
            sp500_companies = sp500_table[['Symbol', 'Security', 'GICS Sector']]
            sp500_companies.columns = ['Symbol', 'Name', 'Sector']
            sp500_companies['Yahoo_Symbol'] = sp500_companies['Symbol'].str.replace('.', '-', regex=False)
            symbol_mapping = sp500_companies.set_index('Yahoo_Symbol')['Symbol'].to_dict()
            yahoo_symbols = sp500_companies['Yahoo_Symbol'].tolist()
            logging.info(f"Fetching data for {len(yahoo_symbols)} companies.")
            features = [
                'marketCap', 'trailingPE', 'trailingEps', 'dividendYield','totalRevenue', 'profitMargins', 'operatingMargins','returnOnAssets', 'returnOnEquity', 'debtToEquity','currentRatio', 'quickRatio']
            data_list = []
            for yahoo_symbol in yahoo_symbols:
                try:
                    ticker = yf.Ticker(yahoo_symbol)
                    info = ticker.info
                    data = {'Yahoo_Symbol': yahoo_symbol, 'Date': datetime.now().date()}
                    for feature in features:
                        data[feature] = info.get(feature)

                    data_list.append(data)
                    logging.info(f"Fetched data for {yahoo_symbol}.")
                except Exception as e:
                    logging.error(f"Failed to fetch data for {yahoo_symbol}. Error: {str(e)}")
            if not data_list:
                logging.error("No data fetched. Exiting.")
                return pd.DataFrame()
            data = pd.DataFrame(data_list)
            data['Symbol'] = data['Yahoo_Symbol'].map(symbol_mapping)
            data = data.merge(sp500_companies, on='Symbol', how='left')
            columns_order = ['Date', 'Symbol', 'Name', 'Sector'] + features
            data = data[columns_order]

            for feature in features:
                data[feature] = pd.to_numeric(data[feature], errors='coerce')
                data[feature] = data.groupby('Sector')[feature].transform(lambda x: x.fillna(x.mean()))

            data.rename(columns={
                'marketCap': 'Market Cap',
                'trailingPE': 'P/E Ratio',
                'trailingEps': 'EPS',
                'dividendYield': 'Dividend Yield',
                'totalRevenue': 'Revenue',
                'profitMargins': 'Profit Margin',
                'operatingMargins': 'Operating Margin',
                'returnOnAssets': 'Return on Assets',
                'returnOnEquity': 'Return on Equity',
                'debtToEquity': 'Debt to Equity',
                'currentRatio': 'Current Ratio',
                'quickRatio': 'Quick Ratio'
            }, inplace=True)

            logging.info("Data fetched successfully.")

            numerical_columns = ['Market Cap', 'P/E Ratio', 'EPS', 'Dividend Yield', 'Revenue', 'Profit Margin', 'Operating Margin', 'Return on Assets', 'Return on Equity', 'Debt to Equity', 'Current Ratio', 'Quick Ratio']
            
            for column in numerical_columns:
                data[column] = data.groupby('Sector')[column].transform(lambda x: x.fillna(x.mean()))
                
            data['P/E Ratio'] = data['P/E Ratio'].replace([np.inf, -np.inf], np.nan)
            data['P/E Ratio'] = data.groupby('Sector')['P/E Ratio'].transform(lambda x: x.fillna(x.mean()))
                        
            self.data_Clustering = data.copy()
            return self.data_Clustering