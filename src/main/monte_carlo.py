import numpy as np
# Monte Carlo simulation for option pricing
def simulate_gbm(S0, r, sigma, T, n_steps, n_paths):
    """
    Simulate stock price paths using Geometric Brownian Motion.
    
    S0: initial stock price
    r: risk-free rate (used as drift under risk-neutral measure)
    sigma: volatility
    T: time to expiry in years
    n_steps: number of timesteps per path
    n_paths: number of simulated paths
    
    Returns: array of shape (n_steps+1, n_paths)
    """
    dt = T / n_steps # time increment
    
    # Initialise price array
    S = np.zeros((n_steps + 1, n_paths)) # +1 to include initial price
    S[0] = S0
    
    # Simulate paths
    for t in range(1, n_steps + 1):
        Z = np.random.standard_normal(n_paths) # standard normal random variables
        S[t] = S[t-1] * np.exp((r - 0.5 * sigma**2) * dt + sigma * np.sqrt(dt) * Z) # GBM formula
    
    return S

def price_european_call(S0, K, r, sigma, T, n_steps=252, n_paths=10000):
    """
    Price a European call option using Monte Carlo simulation.
    """
    S = simulate_gbm(S0, r, sigma, T, n_steps, n_paths)
    
    payoffs = np.maximum(S[-1] - K, 0) # payoff at expiry for each path
    price = np.exp(-r * T) * np.mean(payoffs)    # discount average payoff to today
    
    return price

def price_asian_call(S0, K, r, sigma, T, n_steps=252, n_paths=10000):
    """
    Price an Asian call option using Monte Carlo simulation.
    Payoff based on arithmetic average price over the path.
    """
    S = simulate_gbm(S0, r, sigma, T, n_steps, n_paths)
    
    average_prices = np.mean(S, axis=0) # average price along each path
    payoffs = np.maximum(average_prices - K, 0) # payoff for each path
    price = np.exp(-r * T) * np.mean(payoffs) # discounted expected payoff
    
    return price