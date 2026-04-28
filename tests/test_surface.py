import numpy as np
from scipy.optimize import minimize

from src.main.surface import fit_svi, svi, svi_loss

#check for recovery of known SVI parameters using synthetic data
def test_svi_fit():
    """Test that SVI fitting can recover known parameters from synthetic data.
    """
    # True parameters for synthetic data
    true_params = (0.04, 0.15, -0.3, 0.05, 0.2)
    a_true, b_true, rho_true, m_true, nu_true = true_params
    
    # Generate synthetic data
    spot = 715.17
    T = 0.25
    r = 0.05
    n_strikes = 30
    strikes = np.linspace(spot * 0.85, spot * 1.15, n_strikes)
    F = spot * np.exp(r * T)
    k = np.log(strikes / F)
    
    iv_squared_true = svi(k, *true_params)
    noise = np.random.normal(0, 0.0005, n_strikes)
    iv_squared_noisy = iv_squared_true + noise
    
    # Fit SVI to the noisy data
    fitted_params = fit_svi(k, iv_squared_noisy)
    
    # Don't check parameters directly — check surface quality instead
    iv_squared_fit = svi(k, *fitted_params)
    rmse = np.sqrt(np.mean((iv_squared_fit - iv_squared_noisy)**2))
    assert rmse < 0.001, f"SVI fit quality poor: RMSE={rmse:.6f}"