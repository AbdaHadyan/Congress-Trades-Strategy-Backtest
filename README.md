# Group-Project

# Task List

Accessing Data:
- [x] Scrape data from capitol trades
- [ ] Clean data - estimate value of trades

Analysis and Calculation:
- [ ] Find weighting of each stock per day
- [ ] Store data on trade type and size based on weighting
- [ ] Find value of each trade for fixed intervals
- [ ] Find the return after the 3 year period
- [ ] Test to assess the significance of the difference
- [ ] Other performance metrics i.e. sharp ratio

Data Visualisation:
- [ ] Bar Charts - Politicians with the greatest volume of trades, Stock with the greatest volume of trades
- [ ] Line Graph - Comparison of change in portfolio value over time

Write up
- [ ] Assumption & Methodology
- [ ] Results
- [ ] Conclusion



# Assumptions
- Insider trading occurs, therefore, the stimulant of price changes will occur soon after the traded date. Therefore, the closing position occurs a set period after the traded date. (1M, 3M, 6M)
- Start with an initial wallet of 100K USD
- Performance of the portfolio is representative of years beyond the 3 year period.

# Methodology
- Catagorize each trade based on estimated size. 
- Categories for trade determine the proportion of current wealth to be invested in that position -> value for size to be discussed later. (Categories are as follows: 1K-15K, 15k-50k, 50k-100k...)
