-- Forecast accuracy by region and channel.
select
  d.region,
  d.channel_type,
  sum(f.actual_units) as actual_units,
  sum(f.submitted_forecast_units) as submitted_forecast_units,
  1.0 * (sum(f.submitted_forecast_units) - sum(f.actual_units)) / nullif(sum(f.actual_units), 0) as forecast_variance_pct
from monthly_forecasts f
join dealers d
  on f.dealer_id = d.dealer_id
group by 1, 2
order by abs(forecast_variance_pct) desc;

-- Open compensation exposure by action tier.
select
  risk_tier,
  count(*) as dealer_count,
  sum(open_comp_exposure) as open_comp_exposure,
  avg(priority_score) as avg_priority_score
from dealer_planning_risk
group by 1
order by avg_priority_score desc;

-- Promotion ROI and discounting by channel.
select
  d.channel_type,
  avg(p.expected_roi) as avg_expected_roi,
  avg(s.discount_pct) as avg_discount_pct,
  sum(s.ad_spend) as ad_spend
from promotion_calendar p
join dealers d
  on p.dealer_id = d.dealer_id
join dealer_daily_sales s
  on p.dealer_id = s.dealer_id
group by 1
order by avg_expected_roi desc;

-- Data trust exceptions that should be visible before an executive readout.
select
  event_type,
  severity,
  count(*) as event_count,
  sum(estimated_impact) as estimated_impact
from source_events
where status <> 'Resolved'
group by 1, 2
order by estimated_impact desc;
