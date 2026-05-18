# Data Sources

This project uses synthetic source-style data for a distributor and dealer sales planning workflow in the outdoor power equipment category.

The data is not real company performance. It is generated with `scripts/generate_forecasting_artifact.py` using a fixed random seed so the analysis can be reproduced.

## Generated tables

- `dealers.csv`: 36 channel partners with region, channel type, territory manager, product mix, and baseline demand assumptions.
- `dealer_daily_sales.csv`: 10,944 dealer-day rows from July 2025 through April 2026 with units, revenue, discount, inventory coverage, pipeline units, and advertising spend.
- `monthly_forecasts.csv`: 360 dealer-month forecast submissions and actual unit outcomes.
- `promotion_calendar.csv`: promotion records with offer type, region, channel, advertising spend, and expected ROI.
- `compensation_flags.csv`: incentive and payout review flags with estimated exposure and status.
- `territory_capacity.csv`: weekly manager coverage capacity and coverage risk by region.
- `source_events.csv`: source-system exceptions used to score data quality.
- `recommended_actions.csv`: dealer-level action recommendations produced by the scoring model.

## Modeling assumptions

- Demand has spring seasonality because outdoor power equipment demand rises before and during lawn and landscaping season.
- Channel types have different baseline scale, discount behavior, forecast bias, and incentive exposure.
- Inventory risk increases when high recent sales momentum overlaps with fewer than 18 days of modeled coverage.
- Promotion ROI is modeled by offer type, then adjusted for regional and channel noise.
- Data trust is reduced by unresolved source-system events such as late point-of-sale files, dealer master mismatches, inventory refresh lags, and promotion code gaps.
