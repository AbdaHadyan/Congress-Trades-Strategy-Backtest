import pandas as pd
import numpy as np

from datetime import timedelta,datetime
import matplotlib.pyplot as plt

df = pd.read_csv("Cleaned_Trade_Data.csv")

# need in data cleaning, first change the - character in size, and also get an estimated size

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

df.sort_values(by="Published", ascending=True, inplace=True, ignore_index=True)

wallet = 10000
wallet_size = []


df_positions = pd.DataFrame(columns=["Ticker" , "P0" , "Input Value" , "Close Date"])

# for i in range (10) :
#     closing_positions = df_positions[df_positions["Close Date"] <= df["Published"].iloc[i]]
    



#     for ind,row in  closing_positions.iterrows() :
#         output_value = 0 #p1-p0/po  * inputvalue
#         wallet += output_value
#         df_positions.drop(index=ind, inplace=True)
#         #print(df_positions)

    
#     wallet = wallet - wallet * df["Trade Size"].iloc[i]
#     df_positions.loc[i] = [df["Ticker"].iloc[i] , [],wallet * df["Trade Size"].iloc[i], df["Traded"].iloc[i] + timedelta(days=30)]

#     ##print(df["Published"].iloc[i])

current_day = df["Published"].iloc[0]
while current_day <= datetime.strptime("2022-08-11" , "%Y-%m-%d") :
    try :
        closing_positions = df_positions[df_positions["Close Date"] <= current_day]


        for ind,row in  closing_positions.iterrows() :
            p0 = row["P0"]

            input_value = row["Input Value"]
            output_value = (p1 - p0)/p0 * input_value #p1-p0/po  * inputvalue
            wallet += output_value
            df_positions.drop(index=ind, inplace=True)
            df_positions.reset_index(drop=True,inplace=True)

        open_position = df[df["Published"] == current_day]
        for ind,row in  open_position.iterrows() :
            
            ticker = row["Ticker"] 

            input_value = wallet * row["Trade Size"]
            close_date = row["Traded"] + timedelta(days=30)
            df_positions.append({
                "Ticker": ticker,
                "P0": p0,
                "Input Value": input_value,
                "Close Date": close_date
                }, ignore_index=True)
        wallet_size.append(wallet)
        current_day = current_day + timedelta(days=1)
    except :
        continue

print(wallet_size)

print(df_positions)
print(df.iloc[0:100])