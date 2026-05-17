import csv

with open("data/synthetic_operating_data.csv", newline="") as f:
    rows = list(csv.DictReader(f))

for row in rows:
    score = float(row["channel_growth"]) * 2 + float(row["promo_roi"]) * 10 - float(row["forecast_variance"]) * 1.8 - int(row["comp_flags"]) * 3
    print(f'{row["scenario"]}: scenario_score={score:.1f}')
