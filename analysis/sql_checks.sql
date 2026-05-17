-- Dealer forecast error
select
  dealer_id,
  avg(abs(actual_units - submitted_forecast_units) * 1.0 / nullif(submitted_forecast_units, 0)) as avg_forecast_error
from monthly_forecasts
group by 1;

-- Compensation exposure by dealer
select
  dealer_id,
  count(*) as open_flags,
  sum(estimated_exposure) as open_comp_exposure
from compensation_flags
where status <> 'Resolved'
group by 1
order by open_comp_exposure desc;
