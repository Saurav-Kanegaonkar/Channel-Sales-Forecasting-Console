# Data Dictionary

## `dealers.csv`

- `dealer_id`: Synthetic channel partner identifier.
- `dealer_name`: Synthetic partner name.
- `region`: Sales territory region.
- `channel_type`: Partner channel type.
- `territory_manager`: Synthetic manager name.
- `product_mix`: Primary product category mix.
- `base_daily_units`: Baseline daily demand used by the generator.
- `avg_unit_price`: Modeled average unit price.

## `dealer_daily_sales.csv`

- `date`: Sales date.
- `dealer_id`: Channel partner identifier.
- `units_sold`: Daily units sold.
- `gross_sales`: Modeled daily revenue after discount.
- `discount_pct`: Average discount percent.
- `inventory_days`: Days of inventory coverage.
- `pipeline_units`: Pipeline demand units.
- `ad_spend`: Modeled advertising or co-op support spend.

## `monthly_forecasts.csv`

- `forecast_month`: Forecast month.
- `dealer_id`: Channel partner identifier.
- `submitted_forecast_units`: Units submitted in the forecast.
- `actual_units`: Actual modeled unit demand.
- `forecast_owner`: Team owning the submitted forecast.

## `promotion_calendar.csv`

- `promo_id`: Promotion identifier.
- `start_date`: Promotion start date.
- `dealer_id`: Channel partner identifier.
- `region`: Sales territory region.
- `channel_type`: Partner channel type.
- `promo_type`: Offer or campaign type.
- `expected_roi`: Modeled return on promotion spend.
- `ad_spend`: Modeled campaign support spend.

## `compensation_flags.csv`

- `flag_id`: Compensation review identifier.
- `flag_date`: Flag date.
- `dealer_id`: Channel partner identifier.
- `flag_type`: Incentive or payout issue type.
- `estimated_exposure`: Estimated payout exposure.
- `status`: Open, reviewed, or resolved.

## `territory_capacity.csv`

- `week_start`: Week start date.
- `region`: Sales territory region.
- `manager_capacity_hours`: Available manager coverage hours.
- `active_dealers`: Active partners in territory.
- `coverage_risk`: Low, medium, or high coverage risk.

## `source_events.csv`

- `event_id`: Source-system event identifier.
- `event_date`: Event date.
- `dealer_id`: Channel partner identifier.
- `source_system`: Origin system.
- `event_type`: Exception type.
- `severity`: Low, medium, or high.
- `estimated_impact`: Modeled dollar impact.
- `status`: Open, triaged, or resolved.

## `analysis/outputs/dealer_planning_risk.csv`

- `priority_score`: Explainable action-priority score.
- `risk_tier`: Critical, watch, or stable.
- `forecast_variance_pct`: Forecast minus actual, divided by actual.
- `forecast_accuracy_pct`: Accuracy score derived from absolute forecast variance.
- `recent_sales`: Last 30 modeled sales dollars.
- `sales_momentum_pct`: Last 30 days versus prior 30 days.
- `inventory_days`: Average recent days of inventory coverage.
- `avg_discount_pct`: Average recent discount.
- `promo_roi`: Average expected promotion ROI.
- `open_comp_exposure`: Open incentive exposure.
- `coverage_pressure_pct`: Recent regional coverage pressure.
- `data_quality_score`: Source trust score.
- `recommended_action`: Sales leadership action.
