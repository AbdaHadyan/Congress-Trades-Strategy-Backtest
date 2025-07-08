#imports
from datetime import datetime, timedelta
import pandas as pd

df = pd.read_csv("All_Trade_Data.csv")

df["Ticker"] = df["Ticker"].str.split(":").str[0].replace("/" , "-")

df["Published"] = df["Published"].str.replace("Sept","Sep")
df["Published"] = df["Published"].replace(".*Today.*", datetime.now().strftime("%d %b%Y"), regex=True)
df["Published"] = df["Published"].replace(".*Yesterday.*", (datetime.now() - timedelta(days=1)).strftime("%d %b%Y"), regex=True)
df["Published"] = pd.to_datetime(df["Published"], format= "%d %b%Y")

df["Traded"] = df["Traded"].str.replace("Sept","Sep")
df["Traded"] = df["Traded"].replace(".*Today.*", datetime.now().strftime("%d %b%Y"), regex=True)
df["Traded"] = df["Traded"].replace(".*Yesterday.*", (datetime.now() - timedelta(days=1)).strftime("%d %b%Y"), regex=True)
df["Traded"] = pd.to_datetime(df["Traded"], format= "%d %b%Y")

df["Filed After"] = df["Filed After"].str.replace("days", "")

df = df[df["Price"] != "N/A"]
print("Complete")
df.to_csv("Cleaned_Trade_Data.csv", index=False)