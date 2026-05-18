import csv
import json
import math
import random
from collections import defaultdict
from datetime import date, timedelta
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
OUTPUTS = ROOT / "analysis" / "outputs"
SRC = ROOT / "src"
random.seed(42)

REGIONS = ["North", "South", "Central", "West"]
CHANNELS = ["Independent dealer", "Distributor", "Commercial fleet", "Home center"]
MANAGERS = ["Patel", "Kim", "Nguyen", "Rivera", "Morgan", "Lopez"]
PRODUCT_MIX = ["Pro handheld", "Battery platform", "Parts and service", "Fleet package"]
PROMO_TYPES = ["Rebate", "Bundle", "Co-op advertising", "Spring sell-in"]


def money(value):
    return int(round(value, 0))


def pct(value):
    return round(value, 1)


def write_csv(path, rows, fields):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def month_start(day):
    return day.replace(day=1)


def month_label(day):
    return f"{day.year}-{day.month:02d}"


def daterange(start, end):
    current = start
    while current <= end:
        yield current
        current += timedelta(days=1)


def build_dealers():
    rows = []
    region_weight = {"North": 1.0, "South": 1.12, "Central": 1.05, "West": 1.18}
    channel_weight = {
        "Independent dealer": 1.0,
        "Distributor": 1.35,
        "Commercial fleet": 1.2,
        "Home center": 1.55,
    }
    for idx in range(1, 37):
        region = REGIONS[(idx - 1) % len(REGIONS)]
        channel = CHANNELS[(idx + 1) % len(CHANNELS)]
        base_units = random.randint(36, 116) * region_weight[region] * channel_weight[channel]
        price = random.randint(310, 720) if channel != "Parts and service" else random.randint(120, 260)
        rows.append(
            {
                "dealer_id": f"D{idx:03d}",
                "dealer_name": f"{region} Channel Partner {idx}",
                "region": region,
                "channel_type": channel,
                "territory_manager": MANAGERS[(idx - 1) % len(MANAGERS)],
                "product_mix": PRODUCT_MIX[idx % len(PRODUCT_MIX)],
                "base_daily_units": round(base_units, 2),
                "avg_unit_price": price,
            }
        )
    return rows


def seasonal_factor(day):
    peak = math.exp(-((day.timetuple().tm_yday - 118) ** 2) / (2 * 42**2))
    fall = math.exp(-((day.timetuple().tm_yday - 258) ** 2) / (2 * 56**2))
    return 0.68 + 0.95 * peak + 0.28 * fall


def build_daily_sales(dealers):
    rows = []
    start = date(2025, 7, 1)
    end = date(2026, 4, 30)
    for dealer in dealers:
        base = float(dealer["base_daily_units"])
        price = float(dealer["avg_unit_price"])
        channel = dealer["channel_type"]
        region = dealer["region"]
        channel_discount = {
            "Independent dealer": 0.08,
            "Distributor": 0.13,
            "Commercial fleet": 0.1,
            "Home center": 0.16,
        }[channel]
        for day in daterange(start, end):
            dow = 0.86 if day.weekday() >= 5 else 1.0
            weather = 1 + random.uniform(-0.08, 0.1)
            units = max(4, int(base * seasonal_factor(day) * dow * weather + random.gauss(0, 8)))
            discount = max(2, min(28, random.gauss(channel_discount * 100, 3.2)))
            gross_sales = units * price * (1 - discount / 100)
            inventory_days = max(2, int(random.gauss(25, 10) - seasonal_factor(day) * 6))
            if region == "West" and day.month in [2, 3, 4]:
                inventory_days = max(1, inventory_days - random.randint(2, 7))
            pipeline_units = max(0, int(units * random.uniform(1.2, 3.7)))
            ad_spend = money(gross_sales * random.uniform(0.012, 0.044))
            rows.append(
                {
                    "date": day.isoformat(),
                    "dealer_id": dealer["dealer_id"],
                    "units_sold": units,
                    "gross_sales": money(gross_sales),
                    "discount_pct": pct(discount),
                    "inventory_days": inventory_days,
                    "pipeline_units": pipeline_units,
                    "ad_spend": ad_spend,
                }
            )
    return rows


def build_monthly_forecasts(dealers, daily_sales):
    by_month = defaultdict(int)
    for row in daily_sales:
        by_month[(row["dealer_id"], row["date"][:7])] += int(row["units_sold"])
    rows = []
    for dealer in dealers:
        channel_bias = {
            "Independent dealer": 0.02,
            "Distributor": 0.07,
            "Commercial fleet": -0.03,
            "Home center": 0.1,
        }[dealer["channel_type"]]
        for month in sorted({key[1] for key in by_month if key[0] == dealer["dealer_id"]}):
            actual = by_month[(dealer["dealer_id"], month)]
            miss = random.gauss(channel_bias, 0.105)
            if dealer["region"] == "West" and month in ["2026-02", "2026-03", "2026-04"]:
                miss += 0.07
            submitted = max(1, int(actual * (1 + miss)))
            owner = random.choice(["Sales", "Regional GM", "Finance", "Demand planning"])
            rows.append(
                {
                    "forecast_month": month,
                    "dealer_id": dealer["dealer_id"],
                    "submitted_forecast_units": submitted,
                    "actual_units": actual,
                    "forecast_owner": owner,
                }
            )
    return rows


def build_promotions(dealers):
    rows = []
    idx = 1
    for dealer in dealers:
        for _ in range(random.randint(2, 4)):
            start = date(2025, 10, 1) + timedelta(days=random.randint(0, 205))
            promo_type = random.choice(PROMO_TYPES)
            roi_base = {
                "Rebate": 2.2,
                "Bundle": 2.9,
                "Co-op advertising": 2.5,
                "Spring sell-in": 3.1,
            }[promo_type]
            roi = max(0.7, random.gauss(roi_base, 0.55))
            if dealer["region"] == "West" and dealer["channel_type"] == "Distributor":
                roi -= 0.25
            rows.append(
                {
                    "promo_id": f"PR{idx:03d}",
                    "start_date": start.isoformat(),
                    "dealer_id": dealer["dealer_id"],
                    "region": dealer["region"],
                    "channel_type": dealer["channel_type"],
                    "promo_type": promo_type,
                    "expected_roi": pct(roi),
                    "ad_spend": money(random.randint(2800, 22000)),
                }
            )
            idx += 1
    return rows


def build_compensation_flags(dealers):
    rows = []
    idx = 1
    for dealer in dealers:
        probability = {
            "Independent dealer": 0.28,
            "Distributor": 0.42,
            "Commercial fleet": 0.34,
            "Home center": 0.46,
        }[dealer["channel_type"]]
        for month in range(1, 5):
            if random.random() < probability:
                status = random.choices(["Open", "Reviewed", "Resolved"], weights=[0.42, 0.28, 0.3])[0]
                rows.append(
                    {
                        "flag_id": f"CF{idx:04d}",
                        "flag_date": date(2026, month, random.randint(1, 24)).isoformat(),
                        "dealer_id": dealer["dealer_id"],
                        "flag_type": random.choice(["SPIFF review", "Quota accelerant", "Margin exception", "Duplicate credit"]),
                        "estimated_exposure": money(random.randint(2500, 36000)),
                        "status": status,
                    }
                )
                idx += 1
    return rows


def build_territory_capacity():
    rows = []
    start = date(2025, 7, 7)
    for week in range(44):
        week_start = start + timedelta(days=week * 7)
        for region in REGIONS:
            dealers = {"North": 9, "South": 9, "Central": 9, "West": 9}[region]
            hours = random.randint(42, 72)
            if region == "West" and week_start.month in [2, 3, 4]:
                hours -= random.randint(3, 8)
            ratio = dealers / max(hours, 1)
            if ratio > 0.18:
                risk = "High"
            elif ratio > 0.145:
                risk = "Medium"
            else:
                risk = "Low"
            rows.append(
                {
                    "week_start": week_start.isoformat(),
                    "region": region,
                    "manager_capacity_hours": hours,
                    "active_dealers": dealers,
                    "coverage_risk": risk,
                }
            )
    return rows


def build_source_events(dealers):
    rows = []
    event_types = ["Late POS file", "Forecast override", "Dealer master mismatch", "Promo code gap", "Inventory refresh lag"]
    systems = ["Dealer portal", "ERP", "CRM", "Forecast workbook", "Trade promotion tracker"]
    for idx in range(1, 421):
        dealer = random.choice(dealers)
        event_type = random.choice(event_types)
        severity = random.choices(["Low", "Medium", "High"], weights=[0.48, 0.34, 0.18])[0]
        impact = {"Low": 1500, "Medium": 7200, "High": 18500}[severity] * random.uniform(0.6, 1.45)
        rows.append(
            {
                "event_id": f"EV{idx:04d}",
                "event_date": (date(2025, 7, 1) + timedelta(days=random.randint(0, 303))).isoformat(),
                "dealer_id": dealer["dealer_id"],
                "source_system": random.choice(systems),
                "event_type": event_type,
                "severity": severity,
                "estimated_impact": money(impact),
                "status": random.choices(["Open", "Triaged", "Resolved"], weights=[0.22, 0.28, 0.5])[0],
            }
        )
    return rows


def score_dealers(dealers, daily_sales, forecasts, promotions, comp_flags, capacity, source_events):
    dealer_lookup = {row["dealer_id"]: row for row in dealers}
    daily_by_dealer = defaultdict(list)
    for row in daily_sales:
        daily_by_dealer[row["dealer_id"]].append(row)
    forecasts_by_dealer = defaultdict(list)
    for row in forecasts:
        forecasts_by_dealer[row["dealer_id"]].append(row)
    promo_by_dealer = defaultdict(list)
    for row in promotions:
        promo_by_dealer[row["dealer_id"]].append(row)
    comp_by_dealer = defaultdict(list)
    for row in comp_flags:
        comp_by_dealer[row["dealer_id"]].append(row)
    events_by_dealer = defaultdict(list)
    for row in source_events:
        events_by_dealer[row["dealer_id"]].append(row)
    capacity_by_region = defaultdict(list)
    for row in capacity:
        capacity_by_region[row["region"]].append(row)

    risk_rows = []
    for dealer in dealers:
        dealer_id = dealer["dealer_id"]
        records = sorted(daily_by_dealer[dealer_id], key=lambda item: item["date"])
        last_30 = records[-30:]
        prev_30 = records[-60:-30]
        last_units = sum(int(row["units_sold"]) for row in last_30)
        prev_units = max(1, sum(int(row["units_sold"]) for row in prev_30))
        momentum = (last_units - prev_units) / prev_units * 100
        recent_sales = sum(int(row["gross_sales"]) for row in last_30)
        inventory_days = sum(int(row["inventory_days"]) for row in last_30) / len(last_30)
        avg_discount = sum(float(row["discount_pct"]) for row in last_30) / len(last_30)
        total_actual = sum(int(row["actual_units"]) for row in forecasts_by_dealer[dealer_id])
        total_forecast = sum(int(row["submitted_forecast_units"]) for row in forecasts_by_dealer[dealer_id])
        forecast_variance = (total_forecast - total_actual) / max(1, total_actual) * 100
        forecast_accuracy = max(0, 100 - abs(forecast_variance))
        promo_roi = sum(float(row["expected_roi"]) for row in promo_by_dealer[dealer_id]) / max(1, len(promo_by_dealer[dealer_id]))
        open_comp = sum(int(row["estimated_exposure"]) for row in comp_by_dealer[dealer_id] if row["status"] == "Open")
        event_impact = sum(int(row["estimated_impact"]) for row in events_by_dealer[dealer_id] if row["status"] != "Resolved")
        quality_penalty = min(35, event_impact / 18000)
        quality_score = max(55, 97 - quality_penalty - abs(forecast_variance) * 0.18)
        region_capacity = capacity_by_region[dealer["region"]][-8:]
        high_weeks = sum(1 for row in region_capacity if row["coverage_risk"] == "High")
        coverage_pressure = high_weeks / max(1, len(region_capacity)) * 100
        inventory_risk = max(0, (18 - inventory_days) * 2.3)
        forecast_risk = min(45, abs(forecast_variance) * 1.7)
        comp_risk = min(24, open_comp / 4500)
        promo_risk = max(0, (2.4 - promo_roi) * 8)
        momentum_bonus = max(0, momentum) * 0.2
        score = forecast_risk + inventory_risk + comp_risk + promo_risk + coverage_pressure * 0.16 + quality_penalty + momentum_bonus
        if score >= 58:
            tier = "Critical"
        elif score >= 34:
            tier = "Watch"
        else:
            tier = "Stable"
        if open_comp > 18000:
            action = "Review incentive payout before month close"
        elif inventory_days < 14 and momentum > 6:
            action = "Rebalance coverage and protect constrained supply"
        elif abs(forecast_variance) > 12:
            action = "Reset forecast assumptions with regional owner"
        elif promo_roi < 2.2:
            action = "Pause low-return promotion and test smaller offer"
        elif quality_score < 82:
            action = "Reconcile source feeds before executive readout"
        else:
            action = "Maintain plan and monitor weekly"
        risk_rows.append(
            {
                "dealer_id": dealer_id,
                "dealer_name": dealer_lookup[dealer_id]["dealer_name"],
                "region": dealer["region"],
                "channel_type": dealer["channel_type"],
                "priority_score": round(score, 1),
                "risk_tier": tier,
                "forecast_variance_pct": pct(forecast_variance),
                "forecast_accuracy_pct": pct(forecast_accuracy),
                "recent_sales": money(recent_sales),
                "sales_momentum_pct": pct(momentum),
                "inventory_days": pct(inventory_days),
                "avg_discount_pct": pct(avg_discount),
                "promo_roi": pct(promo_roi),
                "open_comp_exposure": money(open_comp),
                "coverage_pressure_pct": pct(coverage_pressure),
                "data_quality_score": pct(quality_score),
                "recommended_action": action,
            }
        )
    return sorted(risk_rows, key=lambda row: row["priority_score"], reverse=True)


def build_app_payload(dealers, daily_sales, forecasts, promotions, comp_flags, capacity, source_events, risk_rows):
    months = sorted({row["forecast_month"] for row in forecasts})
    trend = []
    for month in months:
        actual = sum(int(row["actual_units"]) for row in forecasts if row["forecast_month"] == month)
        forecast = sum(int(row["submitted_forecast_units"]) for row in forecasts if row["forecast_month"] == month)
        trend.append({"month": month, "actual": actual, "forecast": forecast})

    total_sales = sum(int(row["gross_sales"]) for row in daily_sales)
    total_units = sum(int(row["units_sold"]) for row in daily_sales)
    total_actual = sum(int(row["actual_units"]) for row in forecasts)
    total_forecast = sum(int(row["submitted_forecast_units"]) for row in forecasts)
    forecast_accuracy = max(0, 100 - abs((total_forecast - total_actual) / total_actual * 100))
    open_exposure = sum(int(row["estimated_exposure"]) for row in comp_flags if row["status"] == "Open")
    data_quality = sum(float(row["data_quality_score"]) for row in risk_rows) / len(risk_rows)
    avg_roi = sum(float(row["expected_roi"]) for row in promotions) / len(promotions)

    region_cards = []
    for region in REGIONS:
        region_risks = [row for row in risk_rows if row["region"] == region]
        region_promos = [row for row in promotions if row["region"] == region]
        region_capacity = [row for row in capacity if row["region"] == region][-8:]
        region_cards.append(
            {
                "region": region,
                "avgScore": pct(sum(float(row["priority_score"]) for row in region_risks) / len(region_risks)),
                "forecastVariance": pct(sum(float(row["forecast_variance_pct"]) for row in region_risks) / len(region_risks)),
                "promoRoi": pct(sum(float(row["expected_roi"]) for row in region_promos) / len(region_promos)),
                "coverageRiskWeeks": sum(1 for row in region_capacity if row["coverage_risk"] == "High"),
                "openCompExposure": money(sum(int(row["open_comp_exposure"]) for row in region_risks)),
                "action": max(region_risks, key=lambda row: float(row["priority_score"]))["recommended_action"],
            }
        )

    channel_cards = []
    for channel in CHANNELS:
        channel_risks = [row for row in risk_rows if row["channel_type"] == channel]
        channel_cards.append(
            {
                "channel": channel,
                "avgScore": pct(sum(float(row["priority_score"]) for row in channel_risks) / len(channel_risks)),
                "accuracy": pct(sum(float(row["forecast_accuracy_pct"]) for row in channel_risks) / len(channel_risks)),
                "inventoryDays": pct(sum(float(row["inventory_days"]) for row in channel_risks) / len(channel_risks)),
                "dataQuality": pct(sum(float(row["data_quality_score"]) for row in channel_risks) / len(channel_risks)),
            }
        )

    quality_checks = [
        {
            "check": "Dealer master reconciliation",
            "result": "Watch",
            "detail": f"{sum(1 for row in source_events if row['event_type'] == 'Dealer master mismatch' and row['status'] != 'Resolved')} open or triaged records",
        },
        {
            "check": "Forecast versus actual completeness",
            "result": "Pass",
            "detail": f"{len(forecasts)} monthly dealer forecast records generated",
        },
        {
            "check": "Promotion code integrity",
            "result": "Watch",
            "detail": f"{sum(1 for row in source_events if row['event_type'] == 'Promo code gap' and row['status'] != 'Resolved')} open or triaged records",
        },
        {
            "check": "Inventory refresh freshness",
            "result": "Pass",
            "detail": f"{len(daily_sales)} daily dealer sales rows with inventory coverage",
        },
    ]

    return {
        "summary": {
            "totalSales": money(total_sales),
            "totalUnits": total_units,
            "forecastAccuracy": pct(forecast_accuracy),
            "openCompExposure": money(open_exposure),
            "avgPromoRoi": pct(avg_roi),
            "dataTrust": pct(data_quality),
            "priorityCount": sum(1 for row in risk_rows if row["risk_tier"] != "Stable"),
            "dealerCount": len(dealers),
        },
        "trend": trend,
        "priorityQueue": risk_rows[:14],
        "regions": region_cards,
        "channels": channel_cards,
        "qualityChecks": quality_checks,
        "filters": {
            "regions": ["All regions"] + REGIONS,
            "channels": ["All channels"] + CHANNELS,
        },
    }


def main():
    dealers = build_dealers()
    daily_sales = build_daily_sales(dealers)
    forecasts = build_monthly_forecasts(dealers, daily_sales)
    promotions = build_promotions(dealers)
    comp_flags = build_compensation_flags(dealers)
    capacity = build_territory_capacity()
    source_events = build_source_events(dealers)
    risk_rows = score_dealers(dealers, daily_sales, forecasts, promotions, comp_flags, capacity, source_events)
    payload = build_app_payload(dealers, daily_sales, forecasts, promotions, comp_flags, capacity, source_events, risk_rows)

    write_csv(DATA / "dealers.csv", dealers, list(dealers[0].keys()))
    write_csv(DATA / "dealer_daily_sales.csv", daily_sales, list(daily_sales[0].keys()))
    write_csv(DATA / "monthly_forecasts.csv", forecasts, list(forecasts[0].keys()))
    write_csv(DATA / "promotion_calendar.csv", promotions, list(promotions[0].keys()))
    write_csv(DATA / "compensation_flags.csv", comp_flags, list(comp_flags[0].keys()))
    write_csv(DATA / "territory_capacity.csv", capacity, list(capacity[0].keys()))
    write_csv(DATA / "source_events.csv", source_events, list(source_events[0].keys()))
    write_csv(OUTPUTS / "dealer_planning_risk.csv", risk_rows, list(risk_rows[0].keys()))
    write_csv(OUTPUTS / "priority_queue.csv", risk_rows[:18], list(risk_rows[0].keys()))
    write_csv(
        DATA / "recommended_actions.csv",
        [
            {
                "dealer_id": row["dealer_id"],
                "dealer_name": row["dealer_name"],
                "priority_score": row["priority_score"],
                "risk_tier": row["risk_tier"],
                "recommended_action": row["recommended_action"],
            }
            for row in risk_rows
        ],
        ["dealer_id", "dealer_name", "priority_score", "risk_tier", "recommended_action"],
    )

    (SRC / "data.js").write_text(
        "window.forecastingConsoleData = "
        + json.dumps(payload, indent=2)
        + ";\n",
        encoding="utf-8",
    )
    print(f"Generated {len(daily_sales):,} daily rows, {len(forecasts):,} forecasts, and {len(risk_rows)} scored dealers.")


if __name__ == "__main__":
    main()
