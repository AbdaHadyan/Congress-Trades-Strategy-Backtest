import pandas as pd
import os


raw_trade_data = pd.read_csv(os.path.join("fixed_data", "raw_trades.csv"))
raw_trade_data["trade_id"] = raw_trade_data.index
raw_trade_data["report_date"] = pd.to_datetime(raw_trade_data["report_date"])
raw_trade_data["trade_date"] = pd.to_datetime(raw_trade_data["trade_date"])
raw_trade_data["close_date"] = pd.to_datetime(raw_trade_data["close_date"])

price_data = pd.read_csv(os.path.join("fixed_data", "price_data.csv"))
price_data["date"] = pd.to_datetime(price_data["date"])

def aggregate(trade_data, price_data) :
    """
    Merges price and trade data to assign open and close prices
    Returns:
        aggregate_data (dataframe): columns=["politician_name","ticker","open_price","close_price", "report_date","close_date"] 
    """
    
    open_data = pd.merge_asof(trade_data.sort_values("report_date"), price_data.sort_values("date"), by="ticker", left_on="report_date", right_on="date", direction="forward")
    close_data = pd.merge_asof(trade_data.sort_values("close_date"), price_data.sort_values("date"), by="ticker", left_on="close_date", right_on="date", direction="forward")
    open_data.rename(columns={"price":"open_price"},inplace=True)
    close_data.rename(columns={"price":"close_price"},inplace=True)
    aggregate_data = pd.merge(open_data, close_data[["trade_id", "close_price"]], on=["trade_id"])
    aggregate_data.dropna(inplace=True) 
    aggregate_data.sort_values(by=["report_date","close_date"],inplace=True)
    aggregate_data = aggregate_data[["politician_name","ticker", "est_trade_size", "report_date","open_price","close_date","close_price"]]    

    return aggregate_data
    

aggregate_data = aggregate(raw_trade_data, price_data)

os.makedirs("fixed_data", exist_ok=True)
aggregate_data.to_csv(os.path.join("fixed_data", "aggregate_data.csv"), index=False)
    
print("finished")     