# Channel Sales Forecasting Console

I built this because sales planning conversations often mix forecast variance, promotion response, territory coverage, and compensation risk without a clear way to test tradeoffs. This project turns that conversation into a scenario pack.

![Channel Sales Forecasting Console](docs/images/dashboard.png)

## What this project is

This is a channel sales forecast scenario console using synthetic dealer, promotion, territory, compensation, and forecast data. It lets a sales leader compare base plan, promotion push, and territory rebalance scenarios.

## What makes it different

- Scenario controls that change the forecast readout
- Territory risk cards instead of generic tables
- Recommendation framing for a monthly sales planning meeting
- Methodology and scoring script included with the repo

## Analytical recommendations

- Prefer territory rebalance over a broad promotion push because it lowers forecast variance and compensation risk while preserving ROI.
- Limit promotions to territories with enough coverage to absorb demand.
- Review compensation flags before finalizing the channel forecast.

## Data sources

- Six source-style CSVs now support the channel forecasting scenario pack.
- The data includes dealers, daily sales, promotions, monthly forecasts, territory capacity, and compensation flags.
- The scoring script combines forecast error and unresolved compensation exposure to rank planning risk.

## Repository structure

- `index.html` - interactive scenario pack
- `src/` - scenario data, UI logic, and styling
- `data/` - synthetic operating data
- `analysis/` - methodology, executive findings, SQL checks, and ranked analytical outputs
- `analysis/methodology.md` - scenario scoring assumptions
- `scripts/score_operating_data.py` - channel scenario scoring script
- `docs/images/dashboard.png` - rendered screenshot

## Run locally

```bash
python3 -m http.server 4176
```

Then open `http://localhost:4176`.
