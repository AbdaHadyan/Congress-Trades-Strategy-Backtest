import numpy as np
import pandas as pd
import os

aggregate_data = pd.read_csv(os.path.join("fixed_data", "aggregate_data.csv"))


class calculations () :
    def __init__(self, aggregate_data):
        self.aggregate_data = aggregate_data

    def return_factor(self) :
        self.aggregate_data["return_factor"] = self.aggregate_data["close_price"]/self.aggregate_data["open_price"]


    def trade_size(self) :
        # fixed trade size
        # self.aggregate_data["pct_trade_size"] = 0.05 # every trade has a fixed trade size based on current wallet
        
        

        # top 10 traders - running mean
        # self.aggregate_data["running_return"] = self.aggregate_data.groupby("politician_name")["return_factor"].expanding().mean().reset_index(level=0,drop=True).fillna(0)
        # top_10_trades = self.aggregate_data.groupby("report_date")["running_return"].nlargest(10).index.get_level_values(1)
        # self.aggregate_data = self.aggregate_data.iloc[top_10_trades]
        # self.aggregate_data["pct_trade_size"] = 0
        # self.aggregate_data.loc[top_10_trades, "pct_trade_size"] =  0.05
        
        # top 10 traders - running return/risk
        self.aggregate_data["running_return"] = self.aggregate_data.groupby("politician_name")["return_factor"].expanding().mean().reset_index(level=0,drop=True).fillna(0)
        self.aggregate_data["running_stdev"] = self.aggregate_data.groupby("politician_name")["return_factor"].expanding().std().reset_index(level=0,drop=True).fillna(0)
        self.aggregate_data["running_rr_ratio"] = self.aggregate_data["running_return"]/self.aggregate_data["running_stdev"]
        top_10_trades = self.aggregate_data.groupby("report_date")["running_rr_ratio"].nlargest(10).index.get_level_values(1)
        self.aggregate_data = self.aggregate_data.iloc[top_10_trades]
        self.aggregate_data["pct_trade_size"] = 0
        self.aggregate_data.loc[top_10_trades, "pct_trade_size"] =  0.05
        
    
    def calculate_all(self) :
        self.return_factor()
        self.trade_size()

strategy = "top_10_risk_return"

calculation = calculations(aggregate_data)
calculation.calculate_all()


os.makedirs(os.path.join("analysis_results", strategy), exist_ok=True)

# rename folder for each indiviual trade size strategy
calculation.aggregate_data.to_csv(os.path.join("analysis_results", strategy, f"processed_data_{strategy}.csv"), index=False)

print("finished")