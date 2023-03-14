import yfinance as yf
import pandas as pd

#adj is real exchange rate
if __name__ == "__main__":
    start_date = "2022-01-01"
    end_date = "2022-03-31"

    gold_data = yf.download("GC=F", start=start_date, end=end_date, interval="1d")
    gold_data.index = gold_data.index.date
    gold_data = gold_data[['Open', 'Close']]
    print(type(gold_data))
    mapping = {gold_data.columns[0]: 'Gold Open', gold_data.columns[1]: 'Gold Close'}
    gold_data = gold_data.rename(columns=mapping)
    print(gold_data.columns)

    # download the S&P 500 index data
    sp500_data = yf.download("^GSPC", start=start_date, end=end_date)
    sp500_data = sp500_data[['Open']]
    mapping = {sp500_data.columns[0]: 'S&P 500 Open'}
    sp500_data = sp500_data.rename(columns=mapping)
    print(sp500_data)

    # download the S&P 500 index data
    Usd_Index_data = yf.download("DX-Y.NYB", start=start_date, end=end_date)
    Usd_Index_data = Usd_Index_data[['Open']]
    mapping = {Usd_Index_data.columns[0]: 'USD Index Starting'}
    Usd_Index_data = Usd_Index_data.rename(columns=mapping)
    print(Usd_Index_data)

    # download the S&P 500 index data
    Oil_data = yf.download("CL=F", start=start_date, end=end_date)
    Oil_data = Oil_data[['Open']]
    mapping = {Oil_data.columns[0]: 'Oil open'}
    Oil_data = Oil_data.rename(columns=mapping)
    print(Usd_Index_data)

    # download the S&P 500 index data
    USDToEuro_data = yf.download("CL=F", start=start_date, end=end_date)
    print(USDToEuro_data)
    # USDToEuro_data = USDToEuro_data[['Open']]
    # mapping = {USDToEuro_data.columns[0]: 'Oil open'}
    # USDToEuro_data = USDToEuro_data.rename(columns=mapping)
    # print(Usd_Index_data)

    # concatenate the two DataFrames along the column axis
    combined_data = pd.concat([gold_data, sp500_data,Usd_Index_data,Oil_data], axis=1)

    combined_data.to_excel("gold_data.xlsx")
