import numpy as np
from scipy.optimize import minimize
# SVI surface fitting functions
def prepare_svi_data(calls_clean, spot, r, T):
    clean = calls_clean.dropna(subset=['IV'])
    F = spot * np.exp(r * T)
    k = np.log(clean['strike'] / F)
    iv_squared = clean['IV'] ** 2
    return np.array(k), np.array(iv_squared)

def svi(k, a, b, rho, m, nu):
    """
    SVI implied variance formula.
    k: log-moneyness array
    Returns implied variance (sigma^2) at each k.
    """
    return a + b * (rho * (k - m) + np.sqrt((k - m)**2 + nu**2))

def svi_loss(params, k, iv_squared_market):
    a, b, rho, m, nu = params
    iv_squared_model = svi(k, a, b, rho, m, nu)
    return np.sum((iv_squared_model - iv_squared_market) ** 2)

def fit_svi(k, iv_squared):
    initial_params = [0.04, 0.1, -0.5, 0.0, 0.1]
    
    bounds = [
        (1e-6, 1.0),   # a > 0
        (1e-6, 2.0),   # b > 0
        (-0.999, 0.999), # -1 < rho < 1
        (-2.0, 2.0),   # m unconstrained
        (1e-6, 2.0),   # nu > 0
    ]
    
    result = minimize(svi_loss, initial_params, args=(k, iv_squared), method='L-BFGS-B', bounds=bounds)
    return result.x