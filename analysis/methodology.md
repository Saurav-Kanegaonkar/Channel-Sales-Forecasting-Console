# Methodology

The console ranks channel partners by the probability that sales leadership needs to intervene before the monthly review.

## Inputs

- Forecast variance from monthly submitted forecasts versus actual units.
- Recent sales momentum from the last 30 days compared with the previous 30 days.
- Inventory coverage from daily dealer-level inventory days.
- Promotion return from expected ROI by offer type.
- Compensation exposure from open incentive and payout flags.
- Territory coverage pressure from weekly manager capacity.
- Data trust from unresolved source-system exceptions.

## Scoring model

The model creates a dealer priority score from these components:

- Forecast risk, capped at 45 points.
- Inventory risk when coverage drops below 18 days.
- Open compensation exposure, capped at 24 points.
- Promotion risk when expected ROI falls below 2.4x.
- Territory coverage pressure from recent high-risk weeks.
- Data quality penalty from unresolved exception impact.
- Sales momentum bonus when demand is rising and coverage risk is present.

The score is translated into three tiers:

- Critical: 58 or above.
- Watch: 34 to 57.9.
- Stable: below 34.

## Why this model fits the artifact

The model is intentionally explainable. It is designed for a sales analytics interview discussion where the candidate needs to show forecasting, compensation controls, territory planning, data integrity, and executive communication rather than black-box prediction.
