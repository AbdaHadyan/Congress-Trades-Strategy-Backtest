import yfinance as yf
import os
snp_data = yf.download(["^GSPC"] , start="2022-09-01", end="2025-09-03", interval="1mo")["Close"]
os.makedirs("fixed_data", exist_ok=True)
snp_data.to_csv(os.path.join("fixed_data", "SNP_500_prices.csv"), index=False)
