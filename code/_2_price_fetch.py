import pandas as pd
import yfinance as yf
import time
import os
import numpy as np
# read the files we initially produce



trade_data = pd.read_csv(os.path.join("fixed", "raw_trades.csv"))
trade_data["trade_date"] = pd.to_datetime(trade_data["trade_date"])


def fetch_price_data(trade_data) :
    """
    Downloads price data for batches of ticker symbols
    Returns:
        price_data (dataframe): columns=["date","ticker","price"] 
    """
    price_data = pd.DataFrame([])
    tickers_list = list(trade_data["ticker"].unique())
    ticker_batches = [tickers_list[i:i + 20] for i in range(0, len(tickers_list), 20)]
    start_date = trade_data["trade_date"].min()
    end_date = trade_data["trade_date"].max() + pd.Timedelta(90,"days")
    for batch in ticker_batches:
        try :
            
            data = yf.download(batch, start=start_date, end=end_date)["Close"]
            price_data = pd.concat([price_data, data],axis=1)
            
        except Exception as e:
            print(f"{e} with {batch}")
        time.sleep(1)

    snp_data = yf.download(["^GSPC"] , start=start_date, end=end_date + pd.Timedelta(1,"days") , interval="1mo")["Close"]
    snp_data["return"] = np.log(snp_data["^GSPC"]/snp_data["^GSPC"].shift(1))   

    price_data.reset_index(inplace=True)
    price_data.rename(columns={"Date":"date","Ticker":"ticker","Price":"price"},inplace=True)
    price_data = price_data.melt(id_vars="date", var_name="ticker", value_name="price")
    return price_data, snp_data






price_data, snp_data = fetch_price_data(trade_data) 

os.makedirs("fixed_data", exist_ok=True)
price_data.to_csv(os.path.join("fixed_data", "price_data.csv"), index=False)
snp_data.to_csv(os.path.join("fixed_data", "snp_500_monthly_returns.csv"), index=True)
print("finished")     
