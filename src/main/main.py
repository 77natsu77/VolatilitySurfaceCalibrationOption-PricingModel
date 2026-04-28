from .models import implied_volatility, black_scholes_call
from .data import calls_clean, spot, T
from .surface import prepare_svi_data, fit_svi, svi
import numpy as np
#print(f"main.py: calls_clean has {len(calls_clean)} rows")
#r = 0.05  # risk-free rate proxy, hardcoded for simplicity; in practice, use a more accurate rate
# Test IV on one row manually
#row = calls_clean.iloc[0]
#print(f"Testing: S={spot}, K={row['strike']}, T={T}, mid={row['mid']}")
#print(f"IV result: {implied_volatility(row['mid'], spot, row['strike'], T, r)}")

# USING SYNTHETIC DATA FOR TESTING AS REAL DATA MAY HAVE ISSUES
from .data import generate_synthetic_data
from .surface import fit_svi, svi

spot = 715.17
T = 0.25
r = 0.05

strikes, k, iv, true_params = generate_synthetic_data(spot, T, r)
iv_squared = iv ** 2

print(f"Generated {len(strikes)} synthetic options")
print(f"Strike range: {strikes[0]:.1f} to {strikes[-1]:.1f}")
print(f"IV range: {iv.min():.4f} to {iv.max():.4f}")
print(f"True params: a={true_params[0]}, b={true_params[1]}, rho={true_params[2]}, m={true_params[3]}, nu={true_params[4]}")

params = fit_svi(k, iv_squared)
a, b, rho, m, nu = params

print(f"\nFitted params:  a={a:.4f}, b={b:.4f}, rho={rho:.4f}, m={m:.4f}, nu={nu:.4f}")
print(f"True params:    a=0.0400, b=0.1500, rho=-0.3000, m=0.0500, nu=0.2000")

iv_squared_fit = svi(k, a, b, rho, m, nu)
rmse = np.sqrt(np.mean((iv_squared_fit - iv_squared)**2))
print(f"RMSE: {rmse:.6f}")


import matplotlib.pyplot as plt

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
plt.savefig('vol_smile.png')
print("Plot saved to vol_smile.png")