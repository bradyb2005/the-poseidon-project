from __future__ import annotations

import csv
import os
from typing import Any, Dict, List, Optional, Tuple

# Expected columns for backend/data/food_delivery.csv (33 columns)
EXPECTED_COLUMNS = [
    "order_id",
    "restaurant_id",
    "food_item",
    "order_time",
    "delivery_time",
    "delivery_distance",
    "order_value",
    "delivery_method",
    "traffic_condition",
    "weather_condition",
    "delivery_time_actual",
    "delivery_delay",
    "route_taken",
    "customer_id",
    "age",
    "gender",
    "location",
    "order_history",
    "customer_rating",
    "preferred_cuisine",
    "order_frequency",
    "loyalty_program",
    "food_temperature",
    "food_freshness",
    "packaging_quality",
    "food_condition",
    "customer_satisfaction",
    "small_route",
    "bike_friendly_route",
    "route_type",
    "route_efficiency",
    "predicted_delivery_mode",
    "traffic_avoidance",
]


def default_csv_path() -> str:
    """Return absolute path to backend/data/food_delivery.csv."""
    return os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "data", "food_delivery.csv")
    )


def _parse_bool(value: Any) -> Optional[bool]:
    if value is None:
        return None
    s = str(value).strip().lower()
    if s in {"true", "t", "1", "yes", "y"}:
        return True
    if s in {"false", "f", "0", "no", "n"}:
        return False
    return None


def _to_int(value: Any) -> Optional[int]:
    try:
        return int(str(value).strip())
    except Exception:
        return None


def _to_float(value: Any) -> Optional[float]:
    try:
        return float(str(value).strip())
    except Exception:
        return None


def load_csv(path: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    Loads the food_delivery.csv and returns rows as list[dict].
    Raises FileNotFoundError if the path doesn't exist.
    """
    csv_path = path or default_csv_path()
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"CSV not found at: {csv_path}")

    with open(csv_path, "r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        return [row for row in reader]


def validate_csv(
    path: Optional[str] = None,
    expected_columns: Optional[List[str]] = None,
) -> Tuple[bool, List[str]]:
    """
    Validates:
      - file exists
      - header matches expected columns (same order)
      - basic type checks on first 50 rows

    NOTE: customer_id is allowed to be either numeric OR alphanumeric,
    but it must NOT be blank.
    """
    errors: List[str] = []
    csv_path = path or default_csv_path()
    exp = expected_columns or EXPECTED_COLUMNS

    if not os.path.exists(csv_path):
        return False, [f"CSV not found at: {csv_path}"]

    with open(csv_path, "r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        if reader.fieldnames is None:
            return False, ["CSV has no header row"]

        if list(reader.fieldnames) != exp:
            errors.append("CSV header does not match EXPECTED_COLUMNS exactly")

        rows_checked = 0
        for row in reader:
            rows_checked += 1

            # Required presence checks (string-like allowed)
            cust = row.get("customer_id")
            cust_str = "" if cust is None else str(cust).strip()
            if cust_str == "":
                errors.append(f"customer_id missing/blank at row {rows_checked}")
                break

            # ints
            if _to_int(row.get("restaurant_id")) is None:
                errors.append(f"restaurant_id not int at row {rows_checked}")
                break
            if _to_int(row.get("age")) is None:
                errors.append(f"age not int at row {rows_checked}")
                break

            # floats
            if _to_float(row.get("delivery_distance")) is None:
                errors.append(f"delivery_distance not float at row {rows_checked}")
                break
            if _to_float(row.get("order_value")) is None:
                errors.append(f"order_value not float at row {rows_checked}")
                break
            if _to_float(row.get("route_efficiency")) is None:
                errors.append(f"route_efficiency not float at row {rows_checked}")
                break

            # bool-like
            if _parse_bool(row.get("small_route")) is None:
                errors.append(f"small_route not boolean-like at row {rows_checked}")
                break
            if _parse_bool(row.get("bike_friendly_route")) is None:
                errors.append(f"bike_friendly_route not boolean-like at row {rows_checked}")
                break

            if rows_checked >= 50:
                break

        if rows_checked == 0:
            errors.append("CSV has header but no data rows")

    return len(errors) == 0, errors