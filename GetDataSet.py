from datetime import datetime, timedelta

import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt



# platinum is correlating negatively
# sp 500 has high correlation with usd index. so removed it

def getDataSet(start_date, end_date):
    gold_data = yf.download("GC=F", start=start_date, end=end_date, interval="1d")
    gold_data = gold_data[['Open', 'Close']]
    mapping = {gold_data.columns[0]: 'Gold Open', gold_data.columns[1]: 'Gold Close'}
    gold_data = gold_data.rename(columns=mapping)

    silver_data = yf.download("SIL=F", start=start_date, end=end_date, interval="1d")
    silver_data = silver_data[['Open']]
    mapping = {silver_data.columns[0]: 'Silver Future Open'}
    silver_data = silver_data.rename(columns=mapping)

    # platinum_data = yf.download("PL=F", start=start_date, end=end_date, interval="1d")
    # platinum_data = platinum_data[['Open']]
    # print(type(platinum_data))
    # mapping = {platinum_data.columns[0]: 'Platinum Open'}
    # platinum_data = platinum_data.rename(columns=mapping)
    # print(platinum_data.columns)

    # copper_data = yf.download("HG=F", start=start_date, end=end_date, interval="1d")
    # copper_data = copper_data[['Open']]
    # mapping = {copper_data.columns[0]: 'Copper Open'}
    # copper_data = copper_data.rename(columns=mapping)

    USBond10_data = yf.download("^TNX", start=start_date, end=end_date, interval="1d")
    USBond10_data = USBond10_data[['Open']]
    mapping = {USBond10_data.columns[0]: 'US Bond 10 Y'}
    USBond10_data = USBond10_data.rename(columns=mapping)

    # # download the S&P 500 index data
    # sp500_data = yf.download("^GSPC", start=start_date, end=end_date, interval="1d")
    # sp500_data = sp500_data[['Open']]
    # mapping = {sp500_data.columns[0]: 'S&P 500 Open'}
    # sp500_data = sp500_data.rename(columns=mapping)
    # print(sp500_data)

    # download the S&P 500 index data
    Usd_Index_data = yf.download("DX-Y.NYB", start=start_date, end=end_date, interval="1d")
    Usd_Index_data = Usd_Index_data[['Open']]
    mapping = {Usd_Index_data.columns[0]: 'USD Index Starting'}
    Usd_Index_data = Usd_Index_data.rename(columns=mapping)

    # download the S&P 500 index data
    Oil_data = yf.download("CL=F", start=start_date, end=end_date, interval="1d")
    Oil_data = Oil_data[['Open']]
    mapping = {Oil_data.columns[0]: 'Oil open'}
    Oil_data = Oil_data.rename(columns=mapping)

    # download the S&P 500 index data
    USDToEuro_data = yf.download("USDEUR=X", start=start_date, end=end_date, interval="1d")
    USDToEuro_data = USDToEuro_data[['Open']]
    # USDToEuro_data = USDToEuro_data[['Open']]
    mapping = {USDToEuro_data.columns[0]: 'USD To Euro'}
    USDToEuro_data = USDToEuro_data.rename(columns=mapping)
    # print(Usd_Index_data)

    # download the S&P 500 index data
    USDToINR_data = yf.download("USDINR=X", start=start_date, end=end_date, interval="1d")
    USDToINR_data = USDToINR_data[['Open']]
    # USDToEuro_data = USDToEuro_data[['Open']]
    mapping = {USDToINR_data.columns[0]: 'USD To INR'}
    USDToINR_data = USDToINR_data.rename(columns=mapping)

    # download the S&P 500 index data
    USDToCNY_data = yf.download("USDCNY=X", start=start_date, end=end_date, interval="1d")
    USDToCNY_data = USDToCNY_data[['Open']]
    # USDToEuro_data = USDToEuro_data[['Open']]
    mapping = {USDToCNY_data.columns[0]: 'USD To CNY'}
    USDToCNY_data = USDToCNY_data.rename(columns=mapping)

    # download the S&P 500 index data
    USDToJPY_data = yf.download("USDJPY=X", start=start_date, end=end_date, interval="1d")
    USDToJPY_data = USDToJPY_data[['Open']]
    # USDToEuro_data = USDToEuro_data[['Open']]
    mapping = {USDToJPY_data.columns[0]: 'USD To JPY'}
    USDToJPY_data = USDToJPY_data.rename(columns=mapping)

    # concatenate the two DataFrames along the column axis
    combined_data = pd.concat(
        [Usd_Index_data, Oil_data, USDToEuro_data, USDToINR_data, USDToCNY_data, USDToJPY_data,
         USBond10_data, silver_data, gold_data], axis=1)
    # Drop records that don't have gold close.
    combined_data = combined_data.dropna()
    combined_data = combined_data[(combined_data >= 0).all(1)]
    combined_data.insert(len(combined_data.columns) - 5, 'GoldToOil',
                         (combined_data['Gold Open'] / combined_data['Oil open']))
    return combined_data

if __name__ == "__main__":
    import time

    start_date = "2020-01-01"
    end_date = "2022-04-01"
    # print(f"Start date: {start_date} End date: {end_date}")
    getDataSet(start_date, end_date).to_excel("gold_data.xlsx")


    # # # start_date = "2013-01-01"
    # start_date = "2022-04-08"
    # end_date = "2023-04-08"
    # getDataSet(start_date, end_date).to_excel("gold_data.xlsx")

    # create a function that takes todays date and using timestamp go back in the past.

    # load model.
    # from joblib import load
    #
    # model = load('model.joblib')
