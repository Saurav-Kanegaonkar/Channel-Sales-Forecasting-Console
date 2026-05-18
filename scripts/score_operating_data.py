import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
QUEUE = ROOT / "analysis" / "outputs" / "priority_queue.csv"


with QUEUE.open(newline="") as handle:
    rows = list(csv.DictReader(handle))

print("Top channel sales planning actions")
for row in rows[:10]:
    print(
        f"{row['dealer_id']} | {row['risk_tier']} | score={row['priority_score']} | "
        f"forecast_var={row['forecast_variance_pct']}% | inventory={row['inventory_days']} days | "
        f"action={row['recommended_action']}"
    )
