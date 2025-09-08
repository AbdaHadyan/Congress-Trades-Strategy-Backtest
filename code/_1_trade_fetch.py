import pandas as pd
import requests
from bs4 import BeautifulSoup
import time
import os

size_est = {
    "1K–15K" : 8000, 
    "15K–50K" : 32500,
    "50K–100K"  : 75000,
    "100K–250K" : 175000,
    "250K–500K" : 375000, 
    "500K–1M" : 750000,
    "1M–5M" : 3000000,
    "5M–25M" : 15000000
}


class TradeScraper() :
    def __init__(self):
        self.trade_data = []

    def fetch_page(self, page) :
        """
        Scrapes single page of stock buy trades from Capitol Trades
        Args:
            page (int): the page number to scrape

        Returns:
            Maximum of 96 rows of trades per page
        """
        print(f"Scraping page {page}")
        url = f"https://www.capitoltrades.com/trades?pageSize=96&assetType=stock&txType=buy&country=us&page={page}"
        try :
            response = requests.get(url)
            response.raise_for_status()
        except requests.RequestException as e:
            print(f"Error for fetching {page}: {e}")
            return []
        
        soup = BeautifulSoup(response.text, "html.parser")
        html = soup.select("tbody > tr")

        return html
    
    def page_parser(self, html) :
        """
        Parses trades returned by fetch_page(page) into a readable list
        
        Args:
            html (tag): Elements representing trades
        """
        for row in html :
            try:
                
                politician = row.find("h2", class_="politician-name").text.strip()
                issuer_ticker = row.find("span", class_="q-field issuer-ticker").text.strip()
                dates = row.find_all("div", class_="text-size-3 font-medium")
                years = row.find_all("div", class_="text-size-2 text-txt-dimmer")
                report_date = dates[0].text.strip() + " " + years[0].text.strip()
                trade_date = dates[1].text.strip() + " " + years[1].text.strip()
                tx_type = row.find("span", class_="tx-type").text.strip()
                trade_size = row.find("span", class_="q-field trade-size").text.strip()
                self.trade_data.append({
                    "politician_name" : politician,
                    "ticker" : issuer_ticker,
                    "trade_date": trade_date,
                    "report_date" : report_date,
                    "trade_size" : trade_size,
                    "transaction_type" : tx_type
                })
            except AttributeError :
                break
                

    def fetch_range(self, start_page=2, last_page=117) :
        """
        Scrapes and Parses all available trades
        """
        page = start_page
        while page <= last_page :
            html = self.fetch_page(page)
            if not html :
                break
            self.page_parser(html)
            page +=1

            time.sleep(1)

def data_cleaning(trade_data) :
    """
    Cleans trade data 
    
    Returns:
        cleans data by:
            Modifying ticker symbols for recognition in Yahoo Finance
            Estimating trade size from range
            Converting dates into pd datatime format
            Removing late trades
    """
    
    trade_data["ticker"] = trade_data["ticker"].str.replace(":US","") 
    trade_data["ticker"] = trade_data["ticker"].str.replace("/", "-") 

    trade_data["est_trade_size"] = trade_data["trade_size"].map(size_est)

    trade_data["trade_date"] = trade_data["trade_date"].str.replace("Sept","Sep")
    trade_data["report_date"] = trade_data["report_date"] .str.replace("Sept","Sep")
    
    trade_data["trade_date"] = pd.to_datetime(trade_data["trade_date"], format="%d %b %Y")
    trade_data["report_date"] = pd.to_datetime(trade_data["report_date"], format="%d %b %Y")
    
    trade_data["close_date"] = trade_data["trade_date"] + pd.Timedelta(30 , "days") #### Change for Strategy ####
    trade_data = trade_data[trade_data["close_date"] > trade_data["report_date"]]

    trade_data.reset_index().rename(columns={"index": "trade_id"})
    trade_data.dropna(inplace=True)
    return trade_data

scraping = TradeScraper()
scraping.fetch_range(2,117)

trade_data = pd.DataFrame(scraping.trade_data)
cleaned_trade_data = data_cleaning(trade_data)


os.makedirs("fixed_data", exist_ok=True)
cleaned_trade_data.to_csv(os.path.join("fixed_data", "raw_trades.csv"), index=False)

print("finished")
