# Channel Sales Forecasting Console

I built this because channel sales planning needs an artifact that connects source data, analysis, and recommendations, not just a polished dashboard screenshot.

![Channel Sales Forecasting Console](docs/images/dashboard.png)

## What this project is

This is a scenario artifact for channel sales planning. It uses synthetic but workflow-shaped data to rank dealer-level risks and convert the output into stakeholder-ready recommendations.

## Data sources

- `entities.csv` - 32 dealer records
- `daily_metrics.csv` - 3,840 daily operating rows
- `source_events.csv` - 650 event and exception records
- `recommended_actions.csv` - 180 action candidates

## Analysis outputs

- `analysis/executive_findings.md`
- `analysis/analysis_plan.md`
- `analysis/sql_checks.sql`
- `analysis/outputs/priority_queue.csv`

## Recommendation

Use the priority queue to focus stakeholder attention on the dealer segments where performance upside, measurement risk, and operational readiness overlap.

## Run locally

```bash
python3 -m http.server 4173
```
