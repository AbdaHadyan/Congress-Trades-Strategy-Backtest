import numpy as np
import pandas as pd
import os

strategy = "top_10_risk_return"

processed_data = pd.read_csv(os.path.join("analysis_results", strategy, f"processed_data_{strategy}.csv"))
processed_data["report_date"] = pd.to_datetime(processed_data["report_date"])
processed_data["close_date"] = pd.to_datetime(processed_data["close_date"])

processed_data = processed_data[processed_data["report_date"] > min(processed_data["report_date"]) + pd.Timedelta(90, "days")].reset_index().sort_values(by=["report_date","close_date"],)

class simulation() :
    def __init__(self, wallet):
        self.cost = 0
        self.revenue = 0
        self.wallet = wallet
        
    
    def cashflow_calc(self, row) : # find the cost of the trades (based on pct_trade_size) find the revenue the trade will return (cost * return_factor) and free cash after buy
        self.cost = row.pct_trade_size * self.wallet
        self.revenue = self.cost * row.return_factor
        self.wallet -= self.cost

    def update_transaction_history(self, transaction_history, status, row):
        transaction_history.append({
            "politician_name" : row.politician_name , 
            "ticker" : row.ticker, 
            "date" : row.report_date if status == "open" else row.close_date, 
            "position_status" : status, 
            "cashflow" : -self.cost if status == "open" else row.revenue,
            "profit_loss" : row.profit_loss if status == "close" else 0, 
            "wallet" : self.wallet
        })
        return transaction_history
    
    def update_opened_trades(self, opened_trades, row) :
        
        new_trade = pd.DataFrame({
            "politician_name" : [row.politician_name], 
            "ticker" : [row.ticker], 
            "close_date" : [row.close_date], 
            "revenue" : [self.revenue],
            "profit_loss" : [self.revenue-self.cost]
        })
        opened_trades = pd.concat([opened_trades, new_trade], axis=0,ignore_index=True).sort_values(by=["close_date"])
        return opened_trades
        


    def open_trade(self, transaction_history, opened_trades, open_row) : # add the needed information for an opened trade into the transaction history
        transaction_history = self.update_transaction_history(transaction_history, "open", open_row)
        opened_trades = self.update_opened_trades(opened_trades, open_row)
        return opened_trades, transaction_history
    

    def close_trades(self, transaction_history, pending_close) :
    
        for close_row in pending_close.itertuples() :
            
            self.wallet += close_row.revenue
            self.update_transaction_history(transaction_history, "close", close_row)
           

transaction_history = []
opened_trades = pd.DataFrame(columns=["politician_name","ticker","close_date","revenue","profit_loss"])
wallet = 10000
data_length = len(processed_data)

for open_row in (processed_data.itertuples()) :
    # jan 30
    # buy at jan 30
    # then we close all the ones before jan30
    # jan 30 open
    # jan 15 close
    # jan 16 close
 

    sim = simulation(wallet)
    
    pending_close = opened_trades[opened_trades["close_date"] <= open_row.report_date]
    opened_trades = opened_trades[opened_trades["close_date"] > open_row.report_date]
    sim.close_trades(transaction_history, pending_close)

    sim.cashflow_calc(open_row)
    opened_trades, transaction_history = sim.open_trade(transaction_history, opened_trades, open_row)
    wallet = sim.wallet 
    
pending_close = opened_trades
sim.close_trades(transaction_history, pending_close)


transaction_history = pd.DataFrame(transaction_history)

# rename folder for each indiviual trade size strategy

transaction_history.to_excel(os.path.join("analysis_results", strategy ,f"transaction_history_{strategy}.xlsx"), index=False)
processed_data.to_excel(os.path.join("analysis_results", strategy, f"processed_data_{strategy}.xlsx"), index=False)
print("finished")

