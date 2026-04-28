import matplotlib.pyplot as plt
import numpy as np
import os

from .monte_carlo import price_european_call
from .models import black_scholes_call
from .surface import svi

# Ensure plots directory exists
os.makedirs('plots', exist_ok=True)

def volatility_smile_plot(k, iv, true_params, fitted_params):
    a, b, rho, m, nu = fitted_params
    
    k_plot = np.linspace(k.min(), k.max(), 200)
    iv_fit_plot = np.sqrt(svi(k_plot, a, b, rho, m, nu))
    iv_true_plot = np.sqrt(svi(k_plot, *true_params))

    plt.figure(figsize=(10, 6))
    plt.scatter(k, iv, color='black', label='Synthetic data', zorder=5)
    plt.plot(k_plot, iv_fit_plot, color='blue', label='SVI fit')
    plt.plot(k_plot, iv_true_plot, color='red', linestyle='--', label='True SVI')
    plt.xlabel('Log-moneyness (k)')
    plt.ylabel('Implied Volatility')
    plt.title('SVI Volatility Smile Fit')
    plt.legend()
    plt.grid(True)
    plt.savefig('plots/vol_smile.png')
    print("Plot saved to plots/vol_smile.png")

    
def plot_paths(S, n_display=50): # number of paths to display in the plot, we use 50 to avoid cluttering the plot
    """Plot a subset of simulated GBM paths."""
    import matplotlib.pyplot as plt
    
    plt.figure(figsize=(10, 6))
    plt.plot(S[:, :n_display], alpha=0.3, linewidth=0.8)
    plt.xlabel('Timestep')
    plt.ylabel('Stock Price')
    plt.title('Simulated GBM Paths')
    plt.grid(True)
    plt.savefig('plots/gbm_paths.png')
    print("Saved plots/gbm_paths.png")

def plot_convergence(S0, K, r, sigma, T, bs_price):
    """Plot MC price convergence as n_paths increases."""
    import matplotlib.pyplot as plt
    
    path_counts = [100, 500, 1000, 2000, 5000, 10000, 20000]
    mc_prices = []
    
    for n in path_counts:
        price = price_european_call(S0, K, r, sigma, T, n_paths=n)
        mc_prices.append(price)
    
    plt.figure(figsize=(10, 6))
    plt.plot(path_counts, mc_prices, 'bo-', label='MC price')
    plt.axhline(y=bs_price, color='red', linestyle='--', label='BS price')
    plt.xlabel('Number of paths')
    plt.ylabel('Option price')
    plt.title('Monte Carlo Convergence')
    plt.legend()
    plt.grid(True)
    plt.savefig('plots/convergence.png')
    print("Saved plots/convergence.png")


def volatility_sensitivity_plot(spot, T, r):
    # Sensitivity to volatility
    sigmas = np.linspace(0.1, 0.5, 20)
    bs_prices = [black_scholes_call(S=spot, K=spot, T=T, r=r, sigma=s) for s in sigmas]
    mc_prices = [price_european_call(S0=spot, K=spot, r=r, sigma=s, T=T, n_paths=10000) for s in sigmas]

    plt.figure(figsize=(10, 6))
    plt.plot(sigmas, bs_prices, 'r-', label='Black-Scholes')
    plt.plot(sigmas, mc_prices, 'bo--', label='Monte Carlo')
    plt.xlabel('Volatility (σ)')
    plt.ylabel('Call Price')
    plt.title('Option Price Sensitivity to Volatility')
    plt.legend()
    plt.grid(True)
    plt.savefig('plots/sensitivity_vol.png')
    print("Saved plots/sensitivity_vol.png")