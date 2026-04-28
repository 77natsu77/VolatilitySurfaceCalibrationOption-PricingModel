![CI](https://github.com/77natsu77/VolatilitySurfaceCalibrationOption-PricingModel/actions/workflows/ci.yml/badge.svg)
# Volatility Surface Calibration & Option Pricing Model

A quantitative finance project implementing a full pipeline from live 
market data to implied volatility extraction and volatility surface 
calibration, written in Python.

Built as an independent project to develop practical skills in 
quantitative finance, numerical methods, and financial modelling — 
combining real options data with mathematical pricing theory.

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
- [ ] Phase 3: Volatility surface fitting
- [ ] Phase 4: Monte Carlo simulation and exotic pricing
- [ ] Phase 5: Analysis and documentation

## Concepts Covered
- Call/put options, strike, expiry, moneyness, bid-ask spread
- Black-Scholes formula and its inputs
- Implied volatility via Newton-Raphson root-finding

## Dependencies
pip install yfinance pandas numpy scipy