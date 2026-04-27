from models import implied_volatility, black_scholes_call
from data import calls_clean, spot, T

# Test: if we price an option with sigma=0.2, can we recover 0.2?
test_price = black_scholes_call(S=100, K=100, T=1, r=0.05, sigma=0.2)
iv = implied_volatility(test_price, S=100, K=100, T=1, r=0.05)
#print(f"Test price: {test_price:.4f}")
#print(f"Recovered IV: {iv:.4f}")
#print(f"Expected: 0.2000")

r = 0.05  # risk-free rate proxy

calls_clean['IV'] = calls_clean.apply(
    lambda row: implied_volatility(row['mid'], spot, row['strike'], T, r),
    axis=1
)

print(calls_clean[['strike', 'mid', 'IV']].to_string())