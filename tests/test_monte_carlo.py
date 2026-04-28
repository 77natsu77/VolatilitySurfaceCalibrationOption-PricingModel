from src.main.monte_carlo import price_european_call, price_asian_call
from src.main.models import black_scholes_call

def test_european_call_mc():
    """MC European call should be within 5% of Black-Scholes."""
    bs_price = black_scholes_call(S=100, K=100, T=1, r=0.05, sigma=0.2)
    mc_price = price_european_call(S0=100, K=100, r=0.05, sigma=0.2, T=1, n_paths=50000)
    assert abs(mc_price - bs_price) / bs_price < 0.05, f"MC price {mc_price:.4f} too far from BS {bs_price:.4f}"

def test_asian_call_cheaper_than_european():
    """Asian call must always be cheaper than equivalent European call."""
    european = price_european_call(S0=100, K=100, r=0.05, sigma=0.2, T=1, n_paths=10000)
    asian = price_asian_call(S0=100, K=100, r=0.05, sigma=0.2, T=1, n_paths=10000)
    assert asian < european, f"Asian {asian:.4f} should be cheaper than European {european:.4f}"