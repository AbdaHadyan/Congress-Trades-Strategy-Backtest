
# importing

import pandas as pd
import seaborn as sns
import yfinance as yf
import requests
from bs4 import BeautifulSoup

# data fetching

page = 1
all_trade_data = [['Politician', 'Traded Issuer', 'Published', 'Traded', 'Filed After', 'Owner', 'Type', 'Size', 'Price', '']]
columns = ['Politician', 'Traded Issuer', 'Published', 'Traded', 'Filed After', 'Owner', 'Type', 'Size', 'Price', '']
for i in range(10) :
    print(f"scraping page {page}")
    url = f"https://www.capitoltrades.com/trades?page={page}"
    response = requests.get(url)

    soup = BeautifulSoup(response.text, "html.parser")
    rows = soup.find_all("tr")
    trade_data = []

    for row in rows:
        cells = row.find_all(["td","th"])
        data = [cell.text.strip() for cell in cells]
        if len(data) == 10 and data != columns :
            trade_data.append(data)
    
    if not trade_data :
        break
    
    
    all_trade_data.extend(trade_data)

    page +=1

df = pd.DataFrame(all_trade_data)

df.columns = df.iloc[0]
df = df[1:].drop(columns="")
print(df)

df.to_csv("All_Trade_Data.csv")
