import csv
from collections import defaultdict

forecast_error = defaultdict(list)
with open("data/monthly_forecasts.csv", newline="") as f:
    for row in csv.DictReader(f):
        submitted = int(row["submitted_forecast_units"])
        actual = int(row["actual_units"])
        forecast_error[row["dealer_id"]].append(abs(actual - submitted) / max(submitted, 1))

comp = defaultdict(float)
with open("data/compensation_flags.csv", newline="") as f:
    for row in csv.DictReader(f):
        if row["status"] != "Resolved":
            comp[row["dealer_id"]] += float(row["estimated_exposure"])

ranked = []
for dealer_id, errors in forecast_error.items():
    avg_error = sum(errors) / len(errors)
    score = avg_error * 100 + comp[dealer_id] / 10000
    ranked.append((score, dealer_id, avg_error, comp[dealer_id]))

print("Dealer planning risk")
for score, dealer_id, avg_error, exposure in sorted(ranked, reverse=True)[:10]:
    print(f"{dealer_id}: risk={score:.1f}, forecast_error={avg_error:.1%}, open_comp_exposure=$" + format(exposure, ",.0f"))
