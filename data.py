import yfinance as yf
from datetime import datetime

# --- Fetch Data ---
ticker = yf.Ticker("SPY")
expiry = ticker.options[16]
chain = ticker.option_chain(expiry)

# --- Select calls and compute mid-price ---
calls = chain.calls
calls['mid'] = (calls['bid'] + calls['ask']) / 2

# --- Fetch spot price ---
spot = ticker.fast_info['last_price']

# --- Clean data ---
calls['spread'] = (calls['ask'] - calls['bid']) / calls['mid']
calls_clean = calls[calls['spread'] < 0.10]
calls_clean = calls_clean[calls_clean['volume'] > 0]
calls_clean = calls_clean[(calls_clean['strike'] / spot > 0.8) & 
                           (calls_clean['strike'] / spot < 1.2)]

#print(f"Spot price: {spot:.2f}")
#print(f"Expiry: {expiry}")
#print(f"Clean calls: {len(calls_clean)} rows")
#print(calls_clean[['strike', 'bid', 'ask', 'mid', 'spread', 'volume']].to_string())



expiry_date = datetime.strptime(expiry, "%Y-%m-%d")
today = datetime.today()
T = (expiry_date - today).days / 365

#print(f"T = {T:.4f} years")
#print(f"expiry date: {expiry_date.strftime('%Y-%m-%d')}")