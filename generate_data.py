"""Generate a synthetic pallet-delivery dataset for the analysis.

All values are invented. The shape matches a typical warehouse delivery log:
one row per pallet delivery with planned and actual dates.
Writes data/deliveries.csv, data/warehouses.csv and data/customers.csv.
"""
import csv
import random
from datetime import date, timedelta
from pathlib import Path

random.seed(7)
OUT = Path(__file__).resolve().parent / "data"

WAREHOUSES = [
    ("WH-N", "North", "Delhi"),
    ("WH-S", "South", "Chennai"),
    ("WH-E", "East", "Kolkata"),
    ("WH-W", "West", "Mumbai"),
]
# Each warehouse gets a different on-time profile so the analysis has something to find.
LATE_RATE = {"WH-N": 0.18, "WH-S": 0.08, "WH-E": 0.24, "WH-W": 0.11}
LATE_REASONS = ["Vehicle unavailable", "Customer not ready", "Documentation", "Traffic / route", "Stock not picked"]
REASON_WEIGHTS = {
    "WH-N": [4, 2, 1, 3, 2],
    "WH-S": [1, 3, 1, 2, 1],
    "WH-E": [5, 2, 3, 2, 4],
    "WH-W": [2, 3, 1, 4, 1],
}
SEGMENTS = ["Retail", "FMCG", "Pharma", "E-commerce"]


def main() -> None:
    OUT.mkdir(exist_ok=True)
    customers = [(f"C{n:03d}", random.choice(SEGMENTS)) for n in range(1, 61)]

    with (OUT / "warehouses.csv").open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["warehouse_id", "region", "city"])
        w.writerows(WAREHOUSES)

    with (OUT / "customers.csv").open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["customer_id", "segment"])
        w.writerows(customers)

    start = date(2025, 1, 1)
    rows = []
    delivery_id = 1
    for day in range(365):
        planned = start + timedelta(days=day)
        if planned.weekday() == 4:  # Friday: lighter day
            volume = random.randint(8, 14)
        else:
            volume = random.randint(15, 24)
        # busier run-up to festive season (Oct-Nov)
        if planned.month in (10, 11):
            volume = int(volume * 1.3)
        for _ in range(volume):
            wh = random.choices([w[0] for w in WAREHOUSES], weights=[3, 2, 2, 3])[0]
            cust, _segment = random.choice(customers)
            late_rate = LATE_RATE[wh] * (1.4 if planned.month in (10, 11) else 1.0)
            if random.random() < late_rate:
                delay = random.choices([1, 2, 3, 5], weights=[6, 3, 2, 1])[0]
                reason = random.choices(LATE_REASONS, weights=REASON_WEIGHTS[wh])[0]
            else:
                delay, reason = 0, ""
            status = "Delivered"
            if random.random() < 0.01:
                status, delay, reason = "Cancelled", 0, ""
            actual = "" if status == "Cancelled" else (planned + timedelta(days=delay)).isoformat()
            rows.append([
                f"D{delivery_id:06d}", wh, cust, planned.isoformat(), actual,
                random.randint(1, 6), status, reason,
            ])
            delivery_id += 1

    with (OUT / "deliveries.csv").open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["delivery_id", "warehouse_id", "customer_id", "planned_date",
                    "actual_date", "pallets", "status", "late_reason"])
        w.writerows(rows)
    print(f"Wrote {len(rows)} deliveries to {OUT}")


if __name__ == "__main__":
    main()
