# Volatility Surface Calibration & Option Pricing Model

A quantitative finance project built in Python, implementing a full 
pipeline from raw options data to implied volatility extraction.

## Project Structure
- `data.py` — Fetches and cleans SPY options data via yfinance
- `models.py` — Black-Scholes pricing, Vega, and implied volatility
- `main.py` — Runs the full pipeline

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