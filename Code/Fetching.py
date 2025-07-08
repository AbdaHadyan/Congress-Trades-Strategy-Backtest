# Fetching

# importing

import pandas as pd
import requests
from bs4 import BeautifulSoup

# data fetching

all_trade_data = [['Party', 'Politician','Ticker', 'Traded Issuer', 'Published', 'Traded', 'Filed After', 'Owner', 'Type', 'Size', 'Price', ''] ]


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
        if not cells:
            continue
        span_texts = [cell.find("span").get_text(strip=True) if cell.find("span") else None for cell in cells]
        link_texts = [cell.find("a").get_text(strip=True) if cell.find("a") else None for cell in cells]
        div_texts = [cell.find("div").get_text(strip=True) if cell.find("div") else None for cell in cells]
        
        if not (span_texts[0] and link_texts[0] and div_texts[0]): # Stops loop if page empty
            break

        data = [span_texts[0]] + [link_texts[0]] + [span_texts[1]] + [link_texts[1]] + div_texts[2:]
        if len(data) == 12: # Filters bad rows
            page_data.append(data)

    if not page_data: # Stops loop if page is empty
        break
    
    all_trade_data.extend(page_data)
    
    page +=1

df = pd.DataFrame(all_trade_data)

df.columns = df.iloc[0] # creates header
df = df[1:].drop(columns='') # removes unused column

df.to_csv("All_Trade_Data.csv",index=False)
print(df)
