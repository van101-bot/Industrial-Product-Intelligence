import re
from fractions import Fraction


def normalize_number(value):
    """
    Convert numeric strings, decimals, fractions, and mixed numbers
    into float values.

    Examples:
        "4.5"    -> 4.5
        ".045"   -> 0.045
        "7/8"    -> 0.875
        "4 1/2"  -> 4.5
        "4-1/2"  -> 4.5
        '4.5"'   -> 4.5
    """

    if value is None:
        return None

    if isinstance(value, (int, float)):
        return float(value)

    value = str(value).strip()
    if not value:
        return None

    # Remove inch symbols and similar characters
    value = value.replace('"', "").replace("″", "").strip()

    # Handle mixed fraction with dash: 4-1/2
    dash_match = re.fullmatch(r"(\d+)-(\d+)\s*/\s*(\d+)", value)
    if dash_match:
        whole = int(dash_match.group(1))
        numerator = int(dash_match.group(2))
        denominator = int(dash_match.group(3))
        if denominator == 0:
            return None
        return whole + numerator / denominator

    # Direct decimal/integer
    try:
        return float(value)
    except ValueError:
        pass

    # Simple fraction: 7/8
    try:
        if re.fullmatch(r"\d+\s*/\s*\d+", value):
            return float(Fraction(value.replace(" ", "")))
    except (ValueError, ZeroDivisionError):
        pass

    # Mixed number with space: 4 1/2
    mixed_match = re.fullmatch(r"(\d+)\s+(\d+)\s*/\s*(\d+)", value)
    if mixed_match:
        whole = int(mixed_match.group(1))
        numerator = int(mixed_match.group(2))
        denominator = int(mixed_match.group(3))
        if denominator == 0:
            return None
        return whole + numerator / denominator

    return None


def normalize_dimension(value, unit=None):
    return normalize_number(value)


def normalize_pack_quantity(value):
    """
    Normalize pack quantity into an integer.
    Accepts formats like '10pc', '50 pcs', etc.
    """
    if value is None:
        return None

    value = str(value).lower().strip()
    match = re.search(r"\d+", value)
    if match:
        return int(match.group())
    return None


def normalize_grit(value):
    if value is None:
        return None

    value = str(value).strip()
    if not value:
        return None

    # Normalize whitespace
    value = re.sub(r"\s+", "", value)

    # P150 / p150 / P 150
    match = re.fullmatch(r"[Pp](\d+)", value)
    if match:
        return f"P{match.group(1)}"

    # If only number, convert to P-number
    if re.fullmatch(r"\d+", value):
        return f"P{value}"

    return value


def normalize_attribute_record(attributes: dict) -> dict:
    if attributes is None:
        return {}

    normalized = dict(attributes)

    # Numeric dimensions
    dimension_fields = ["diameter", "thickness", "arbor", "length", "width", "height"]
    for field in dimension_fields:
        if field in normalized:
            normalized[field] = normalize_number(normalized[field])

    # Abrasive grade
    if "abrasive_grade" in normalized:
        normalized["abrasive_grade"] = normalize_grit(normalized["abrasive_grade"])
    if "grit" in normalized:
        normalized["grit"] = normalize_grit(normalized["grit"])

    # Pack quantity
    if "pack_quantity" in normalized:
        normalized["pack_quantity"] = normalize_pack_quantity(normalized["pack_quantity"])

    return normalized
