import pandas as pd
from datetime import timedelta, datetime
import yfinance as yf
import time
import sqlite3

df = pd.read_csv("Cleaned_Trade_Data.csv")

df = df.dropna(subset=["Ticker"])
df["Traded"] = pd.to_datetime(df["Traded"])

min_date = df["Traded"].min().strftime("%Y-%m-%d")
max_date = df["Traded"].max().strftime("%Y-%m-%d")

tickers = df["Ticker"].unique().tolist()

batch_size = 50
sleep_time = 2  # seconds between batches
all_close_data = pd.DataFrame()
failed_tickers = []


for i in range(0, len(tickers), batch_size):
    batch = tickers[i:i + batch_size]
    print(f"Downloading batch {i//batch_size + 1}: {batch}")

    try:
        download_data = yf.download(
            tickers=batch,
            start=min_date,
            end=max_date,
            group_by="Ticker",
            auto_adjust=False,
            progress=False
        )

        if len(batch) == 1:
            close = download_data['Close'].to_frame()
            close.columns = batch 

        else:
            close = pd.concat({ticker: download_data[ticker]['Close'] for ticker in batch if ticker in download_data.columns.levels[0]}, axis=1)

        all_close_data = all_close_data.join(close, how='outer')

    except Exception as e:
        print(f"Batch failed: {e}")
        failed_tickers.extend(batch)

    time.sleep(sleep_time)


all_close_data.to_csv("Close_Price_Data.csv",index=False)
conn = sqlite3.connect("Close_Price_Data.db")  # this creates the DB file
all_close_data.reset_index(inplace=True)   # ensure 'Date' becomes a column, not index
all_close_data.to_sql("Close Price", conn, if_exists="replace", index=False)
conn.close()

available_tickers = all_close_data.columns.to_list()
df = df[df["Ticker"].isin(available_tickers)]

df.to_csv("Cleaned_Trade_Data.csv",index=False)


conn = sqlite3.connect("Cleaned_Trade_Data.db")  # this creates the DB file
df.reset_index(inplace=True)   # ensure 'Date' becomes a column, not index
df.to_sql("Cleaned Data", conn, if_exists="replace", index=False)
conn.close()


if failed_tickers:
    pd.Series(failed_tickers).drop_duplicates().to_csv("failed_tickers.csv", index=False)