#imports
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
import sqlite3
df = pd.read_csv("All_Trade_Data.csv")

df["Ticker"] = df["Ticker"].str.split(":").str[0]
df["Ticker"] = df["Ticker"].str.replace("/" , "-")

df["Published"] = df["Published"].str.replace("Sept","Sep")
df["Published"] = df["Published"].replace(".*Today.*", datetime.now().strftime("%d %b%Y"), regex=True)
df["Published"] = df["Published"].replace(".*Yesterday.*", (datetime.now() - timedelta(days=1)).strftime("%d %b%Y"), regex=True)
df["Published"] = pd.to_datetime(df["Published"], format= "%d %b%Y")

df["Traded"] = df["Traded"].str.replace("Sept","Sep")
df["Traded"] = df["Traded"].replace(".*Today.*", datetime.now().strftime("%d %b%Y"), regex=True)
df["Traded"] = df["Traded"].replace(".*Yesterday.*", (datetime.now() - timedelta(days=1)).strftime("%d %b%Y"), regex=True)
df["Traded"] = pd.to_datetime(df["Traded"], format= "%d %b%Y")

df["Filed After"] = df["Filed After"].str.replace("days", "") 


trade_size = {
    "1K–15K" : np.log10(8000)/1000, 
    "15K–50K" : np.log10(32500)/1000,
    "50K–100K"  : np.log10(75000)/1000,
    "100K–250K" : np.log10(175000)/1000,
    "250K–500K" : np.log10(375000)/1000, 
    "500K–1M" : np.log10(750000)/1000,
    "1M–5M" : np.log10(3000000)/1000,
    "5M–25M" : np.log10(15000000)/1000
}
df["Trade Size"] = df["Size"].apply(lambda size:trade_size.get(size))
df["Published"] = pd.to_datetime(df["Published"])
df["Traded"] = pd.to_datetime(df["Traded"])

print(df)

df.sort_values(by="Published", ascending=True, inplace=True, ignore_index=True)



df = df[df["Price"] != "N/A"]
print("Complete")

df.to_csv("Cleaned_Trade_Data.csv")

conn = sqlite3.connect("Cleaned_Trade_Data.db")  # this creates the DB file
df.reset_index(inplace=True)   # ensure 'Date' becomes a column, not index
df.to_sql("Cleaned Data", conn, if_exists="replace", index=False)
conn.close()



