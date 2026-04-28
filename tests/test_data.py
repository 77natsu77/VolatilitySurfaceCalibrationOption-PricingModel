from src.main.data import generate_synthetic_data
import numpy as np

def test_generate_synthetic_data():
    """Test that synthetic data generation produces reasonable outputs."""
    np.random.seed(42)  # for reproducibility
    spot = 715.17
    T = 0.25
    r = 0.05
    strikes, k, iv, true_params = generate_synthetic_data(spot, T, r)
    
    assert len(strikes) == len(k) == len(iv) == 30, "Should generate 30 strikes, log-moneyness, and IVs"
    assert strikes[0] < spot < strikes[-1], "Strikes should be around the spot price"
    assert iv.min() > 0, "IV should be positive"
    assert len(true_params) == 5, "Should return 5 SVI parameters"