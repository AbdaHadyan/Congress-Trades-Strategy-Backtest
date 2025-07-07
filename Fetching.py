# Fetching

# importing

import pandas as pd
import requests
from bs4 import BeautifulSoup

# data fetching

all_trade_data = [['Politician', 'Traded Issuer', 'Published', 'Traded', 'Filed After', 'Owner', 'Type', 'Size', 'Price', '']]
headers = ['Politician', 'Traded Issuer', 'Published', 'Traded', 'Filed After', 'Owner', 'Type', 'Size', 'Price', ''] 

page = 1
while True:
    print(f"scraping page {page}") 
    url = f"https://www.capitoltrades.com/trades?assetType=stock&page={page}" # URL from Capitol Trades, filtered to remove non-stock trades
    response = requests.get(url)

    soup = BeautifulSoup(response.text, "html.parser") # Parses HTML
    rows = soup.find_all("tr") # Finds Trade rows
    page_data = []

    for row in rows:
        cells = row.find_all("td")
        data = [cell.text.strip() for cell in cells] # Removes all whitespace characters in the html
        if len(data) == 10 and data != headers: # Filters bad rows, and headers from each page
            page_data.append(data)
    
    if not page_data: # Stops loop if page is empty
        break
    
    all_trade_data.extend(page_data)

    page +=1

df = pd.DataFrame(all_trade_data)

df.columns = df.iloc[0] # creates header
df = df[1:].drop(columns='') # removes unused column

df.to_csv("All_Trade_Data.csv") 
