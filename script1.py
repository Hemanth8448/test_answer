from typing import Any, Dict, Iterable, List, Optional
import math

def _to_valid_temp(x: Any) -> Optional[float]:
    if x is None:
        return None

    # Convert numeric strings; keep ints/floats as-is
    try:
        val = float(x)
    except (TypeError, ValueError):
        return None

    # Filter out NaN/Inf
    if not math.isfinite(val):
        return None

    # Corruption threshold
    if val < -100:
        return None

    return val


def _extract_candidate_readings(raw: Any) -> Iterable[Any]:
    # Case 1: a plain list/tuple of readings
    if isinstance(raw, (list, tuple)):
        return raw

    # Case 2/3: a dict with either "temps" or "records"
    if isinstance(raw, dict):
        if "temps" in raw:
            return raw.get("temps", [])
        if "records" in raw:
            candidates = []
            for rec in raw.get("records", []):
                # Expect something like [timestamp, temp]
                if isinstance(rec, (list, tuple)) and len(rec) >= 2:
                    candidates.append(rec[1])   # pick the temperature slot
                # else: missing temperature -> ignore
            return candidates

    # Unknown format -> no readings
    return []


def compute_average_temperature(city_data: Dict[str, Any]) -> Dict[str, float]:
    result: Dict[str, float] = {}

    for city, raw in city_data.items():
        # Step A: normalize to candidate values
        candidates = _extract_candidate_readings(raw)

        # Step B: validate/convert each candidate into a float temperature
        valid = []
        for c in candidates:
            v = _to_valid_temp(c)
            if v is not None:
                valid.append(v)

        # Step C: if any valid values, compute rounded mean
        if valid:
            avg = round(sum(valid) / len(valid), 1)
            result[city] = avg
        # else: city omitted per the spec

    return result
city_data = {
    "London": [18.2, "19.7", None, -999, 20.1],
    "Leeds": {"temps": [16.0, 15.4, "error"]},
    "Bristol": {"records": [["2023-07-24T09:00", 18.5],
                            ["2023-07-24T10:00", None],
                            ["2023-07-24T11:00"]]},
    "Oxford": {"records": [["09:00", 21.5], ["10:00", 20.8], ["11:00", "N/A"]]},
    "Hull": [],
    "Bath": {"temps": []}
}

print(compute_average_temperature(city_data))

