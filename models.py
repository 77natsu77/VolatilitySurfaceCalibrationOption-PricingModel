from scipy.stats import norm
import numpy as np

def black_scholes_call(S, K, T, r, sigma):
    """
    Returns theoretical price of a European call option.
    S: spot price
    K: strike price
    T: time to expiry in years
    r: risk-free rate (annualised)
    sigma: volatility (annualised)
    """
    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    
    call_price = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
    return call_price

def vega(S, K, T, r, sigma):
    """
    Returns vega — sensitivity of call price to volatility.
    """
    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    return S * norm.pdf(d1) * np.sqrt(T)

def implied_volatility(market_price, S, K, T, r):
    """
    Returns implied volatility using Newton-Raphson method.
    market_price: observed mid-price from market
    """
    sigma = 0.2  # initial guess — 20% is a reasonable starting point
    
    for i in range(100):  # maximum 100 iterations
        price = black_scholes_call(S, K, T, r, sigma)
        v = vega(S, K, T, r, sigma)

        if v < 1e-10:  # vega too small — division unstable
            return np.nan
        
        diff = price - market_price  # how far is our price from market?
        sigma = sigma - diff / v     # Newton-Raphson update step

        if sigma <= 0:  # sigma must be positive
            return np.nan
              
        if abs(diff) < 1e-6:   # close enough — stop iterating
            return sigma
    
    return np.nan  # failed to converge