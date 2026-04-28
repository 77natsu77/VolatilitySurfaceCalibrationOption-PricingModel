from .data import generate_synthetic_data
from .models import black_scholes_call
from .surface import fit_svi, svi
from .monte_carlo import simulate_gbm, price_european_call, price_asian_call
from .plots import volatility_smile_plot, plot_paths, plot_convergence, volatility_sensitivity_plot
import matplotlib.pyplot as plt
import numpy as np

# USING SYNTHETIC DATA FOR TESTING AS REAL DATA MAY HAVE ISSUES


# Generate synthetic data
spot = 715.17
T = 0.25
r = 0.05

strikes, k, iv, true_params = generate_synthetic_data(spot, T, r)
iv_squared = iv ** 2
# Print summary of synthetic data
print(f"Generated {len(strikes)} synthetic options")
print(f"Strike range: {strikes[0]:.1f} to {strikes[-1]:.1f}")
print(f"IV range: {iv.min():.4f} to {iv.max():.4f}")
print(f"True params: a={true_params[0]}, b={true_params[1]}, rho={true_params[2]}, m={true_params[3]}, nu={true_params[4]}")

# Fit SVI to synthetic data
fitted_params = fit_svi(k, iv_squared)
a, b, rho, m, nu = fitted_params
# Print fitted parameters and compare to true parameters
print(f"\nFitted params:  a={a:.4f}, b={b:.4f}, rho={rho:.4f}, m={m:.4f}, nu={nu:.4f}")
print(f"True params:    a=0.0400, b=0.1500, rho=-0.3000, m=0.0500, nu=0.2000")
# Calculate RMSE of fit
iv_squared_fit = svi(k, a, b, rho, m, nu)
rmse = np.sqrt(np.mean((iv_squared_fit - iv_squared)**2))
print(f"RMSE: {rmse:.6f}")

# Simulate paths of stock price using GBM and price a European call option
S = simulate_gbm(S0=spot, r=r, sigma=0.2, T=T, n_steps=252, n_paths=1000)
# Print summary of simulated paths
print(f"Path array shape: {S.shape}")
print(f"Initial price (all paths): {S[0, 0]:.2f}")
# the mean of simulated final prices should be close to the theoretical expected price S₀·e^(rT).
print(f"Final prices - mean: {S[-1].mean():.2f}, std: {S[-1].std():.2f}")
print(f"Expected final price (theory): {spot * np.exp(r * T):.2f}")

# Price a European call option using Monte Carlo and compare to Black-Scholes
# Never exactly the same due to randomness in Monte Carlo simulations, but should be close with enough paths
K = spot  # ATM option
mc_price = price_european_call(S0=spot, K=K, r=r, sigma=0.2, T=T, n_paths=10000)
bs_price = black_scholes_call(S=spot, K=K, T=T, r=r, sigma=0.2)
asian_price = price_asian_call(S0=spot, K=K, r=r, sigma=0.2, T=T, n_paths=10000)

print(f"Monte Carlo price: {mc_price:.4f}")
print(f"Black-Scholes price: {bs_price:.4f}")
print(f"Asian option price: {asian_price:.4f}")
print(f"Difference between Black-Scholes and European call: {abs(mc_price - bs_price):.4f}")
print(f"Difference between Asian and European call: {abs(asian_price - bs_price):.4f}")

# Plotting
S = simulate_gbm(S0=spot, r=r, sigma=0.2, T=T, n_steps=252, n_paths=1000)

volatility_smile_plot(k, iv, true_params, fitted_params)
plot_paths(S)
plot_convergence(S0=spot, K=spot, r=r, sigma=0.2, T=T, bs_price=bs_price)
volatility_sensitivity_plot(spot, T, r)