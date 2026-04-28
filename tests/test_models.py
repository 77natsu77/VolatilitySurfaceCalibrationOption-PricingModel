from src.main.models import black_scholes_call, implied_volatility

# Very basic tests for our models.py functions. In a real project, we'd want more comprehensive tests, but this is a start.
def test_implied_volatility():
    """Test that implied volatility function can recover known volatility."""
    # Test: if we price an option with sigma=0.2, can we recover 0.2?
    test_price = black_scholes_call(S=100, K=100, T=1, r=0.05, sigma=0.2)
    iv = implied_volatility(test_price, S=100, K=100, T=1, r=0.05)
    assert abs(iv - 0.2) < 1e-6, f"Expected IV close to 0.2, got {iv}"

def test_implied_volatility_non_convergence():
    """Test that implied volatility returns NaN when it fails to converge."""
    # Use a market price that is very unlikely to be produced by any reasonable volatility
    market_price = 1000  # unrealistically high price
    iv = implied_volatility(market_price, S=100, K=100, T=1, r=0.05)
    assert iv != iv, "Expected NaN for non-converging implied volatility"  # NaN is not equal to itself

def test_black_scholes_call_edge_cases():
    """Test black-scholes call function with edge cases."""
    # Deep in-the-money option
    price = black_scholes_call(S=110, K=100, T=1, r=0.05, sigma=0.2)
    assert price > 0, "Expected positive price for deep ITM option"

    # At-the-money option
    price = black_scholes_call(S=100, K=100, T=1, r=0.05, sigma=0.2)
    assert price > 0, "Expected positive price for ATM option"

    # Out-of-the-money option
    price = black_scholes_call(S=90, K=100, T=1, r=0.05, sigma=0.2)
    assert price > 0, "Expected positive price for OTM option"

def test_black_scholes_call_returns_0():
    """Test that black-scholes call function returns 0 for certain edge cases."""
    # Out-of-the-money option with very low stock price
    # Test that black_scholes_call returns 0 when T=0 and the option is OTM (no time left, no intrinsic value)
    price = black_scholes_call(S=50, K=100, T=0, r=0.05, sigma=0.2)
    assert price == 0, "Expected zero price for deeply OTM option with no time left"

def test_vega_positive():
    """Test that vega is positive for reasonable inputs."""
    # Test that vega returns a positive number for a valid ATM option
    from src.main.models import vega
    v = vega(S=100, K=100, T=1, r=0.05, sigma=0.2)
    assert v > 0, "Expected positive vega for reasonable inputs"