![CI](https://github.com/77natsu77/VolatilitySurfaceCalibrationOption-PricingModel/actions/workflows/ci.yml/badge.svg)
# Volatility Surface Calibration & Option Pricing Model

A quantitative finance project implementing a full pipeline from live 
market data to implied volatility extraction and volatility surface 
calibration, written in Python.

Built independently as a self-directed learning project, using an AI 
mentor (Claude) for guided instruction on quantitative finance concepts 
and Python implementation. All code written and understood by the author; 
AI used in a teaching capacity rather than for code generation.

## Motivation
Options markets imply a different volatility for every strike and 
expiry — the so-called volatility surface. This project builds the 
tooling to extract, calibrate, and visualise that surface from live 
SPY options data, then uses it to price exotic options via Monte Carlo 
simulation.

## Project Structure
- `data.py` — Fetches and cleans SPY options data via yfinance
- `models.py` — Black-Scholes pricing, Vega, and implied volatility
- `main.py` — Runs the full pipeline

## Testing
Tests are written using `pytest` and cover individual components in isolation.

Run all tests with:
```bash
pytest tests/
```

## Phases
- [x] Phase 1: Data pipeline (fetch, clean, filter options data)
- [x] Phase 2: Black-Scholes implementation and implied volatility extraction
- [x] Phase 3: Volatility surface fitting
- [x] Phase 4: Monte Carlo simulation and exotic pricing
- [x] Phase 5: Analysis and documentation

## Results

### Volatility Smile
SVI parameterisation fitted to synthetic SPY options data, capturing 
the characteristic left skew observed in equity markets — higher implied 
volatility at lower strikes reflecting demand for downside protection.

### Monte Carlo Validation
European call prices produced by Monte Carlo simulation converge to 
Black-Scholes analytical prices as path count increases, consistent 
with the theoretical 1/√n convergence rate.

### Exotic Pricing
Asian call option priced at approximately 45% below the equivalent 
European call, reflecting the variance-reducing effect of price averaging 
over the path.

### Known Limitations
- Real market data pipeline limited by yfinance data quality; 
  synthetic data used for surface fitting
- Single expiry fitted; full surface requires multiple maturities
- No variance reduction techniques implemented (antithetic variates etc.)

## Concepts Covered
- Call/put options, strike price, expiry, moneyness, bid-ask spread
- Black-Scholes formula: derivation intuition, inputs, and limitations
- Implied volatility extraction via Newton-Raphson root-finding
- Volatility smile and skew; SVI (Stochastic Volatility Inspired) parameterisation
- Geometric Brownian Motion (GBM) and risk-neutral pricing
- Monte Carlo simulation: path generation, convergence, and variance
- Exotic option pricing: Asian options (no closed-form solution)
- Sensitivity analysis and model validation

## Dependencies
Install all dependencies with:
```bash
pip install -r requirements.txt
```
