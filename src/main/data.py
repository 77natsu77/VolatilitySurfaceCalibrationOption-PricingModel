import yfinance as yf
from datetime import datetime
def generate_synthetic_data(spot, T, r, n_strikes=30):
    """
    Generate synthetic options data using a known SVI surface.
    True parameters: a=0.04, b=0.15, rho=-0.3, m=0.05, nu=0.2
    """
    import numpy as np
    # Generate strikes around spot
    strikes = np.linspace(spot * 0.85, spot * 1.15, n_strikes)
    F = spot * np.exp(r * T)
    k = np.log(strikes / F)
    
    # True SVI parameters — we'll try to recover these
    true_params = (0.04, 0.15, -0.3, 0.05, 0.2)
    a, b, rho, m, nu = true_params
    
    # Generate true implied variance then add small noise
    iv_squared_true = a + b * (rho * (k - m) + np.sqrt((k - m)**2 + nu**2))
    noise = np.random.normal(0, 0.0005, n_strikes)
    iv_squared_noisy = iv_squared_true + noise
    
    iv = np.sqrt(np.clip(iv_squared_noisy, 1e-6, None))
    
    return strikes, k, iv, true_params

# --- Fetch Data ---
ticker = yf.Ticker("SPY")
# Select expiry by date rather than index
target_expiry = "2026-05-15"
if target_expiry in ticker.options:
    expiry = target_expiry
else:
    expiry = ticker.options[14]  # fallback
    
#print(f"Using expiry: {expiry}")
chain = ticker.option_chain(expiry)

# --- Select calls and compute mid-price ---
#calls = chain.calls
calls = chain.puts
chain = ticker.option_chain(expiry)
calls = chain.calls
#print(f"Total rows: {len(calls)}")
#print(calls[['strike', 'bid', 'ask', 'volume']].to_string())
calls['mid'] = (calls['bid'] + calls['ask']) / 2

# --- Fetch spot price ---
spot = ticker.fast_info['last_price']
#print(calls[['strike', 'bid', 'ask', 'volume']].to_string())
# --- Clean data ---
calls = calls[(calls['bid'] > 0) & (calls['ask'] > 0)]  # remove unquoted strikes
calls['spread'] = (calls['ask'] - calls['bid']) / calls['mid'] # relative spread
calls_clean = calls[calls['spread'] < 0.20] # remove options with >20% spread, likely illiquid
calls_clean = calls_clean[calls_clean['volume'] > 0] # remove illiquid options 
calls_clean = calls_clean[(calls_clean['strike'] / spot > 0.7) & # remove deep ITM and OTM options
                           (calls_clean['strike'] / spot < 1.3)]

#print(f"Data cleaned: {len(calls_clean)} options remain after filtering.")
#print(f"Additional info: spot={spot}, expiry={expiry}, strike range={calls_clean['strike'].min()}-{calls_clean['strike'].max()}")
expiry_date = datetime.strptime(expiry, "%Y-%m-%d")
today = datetime.today()
T = (expiry_date - today).days / 365

# print out ticker.options to verify we have the right expiry
#print(f"Available expiries: {ticker.options}")
#print(f"Using expiry: {expiry} (T={T:.4f} years)")