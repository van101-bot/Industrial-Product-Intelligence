import re
from fractions import Fraction


def normalize_number(value):

    if value is None:
        return None

    if isinstance(value, (int, float)):
        return float(value)

    value = str(value).strip()

    if not value:
        return None

    # Direct decimal/integer
    try:
        return float(value)
    except ValueError:
        pass

    # Fraction such as 7/8
    try:
        return float(Fraction(value))
    except (ValueError, ZeroDivisionError):
        pass

    # Mixed number such as 4 1/2
    mixed_match = re.fullmatch(
        r"(\d+)\s+(\d+)\s*/\s*(\d+)",
        value,
    )

    if mixed_match:

        whole = int(mixed_match.group(1))
        numerator = int(mixed_match.group(2))
        denominator = int(mixed_match.group(3))

        if denominator == 0:
            return None

        return whole + numerator / denominator

    return None


def normalize_dimension(value, unit=None):

    number = normalize_number(value)

    if number is None:
        return None

    return {
        "value": number,
        "unit": unit or "in",
    }


def normalize_pack_quantity(value):

    number = normalize_number(value)

    if number is None:
        return None

    return int(number)


def normalize_attribute_record(attributes: dict) -> dict:

    normalized = dict(attributes)

    dimension_fields = [
        "diameter",
        "thickness",
        "arbor",
        "length",
        "width",
        "height",
    ]

    for field in dimension_fields:

        if field in normalized:
            normalized[field] = normalize_number(
                normalized[field]
            )

    if "pack_quantity" in normalized:

        normalized["pack_quantity"] = (
            normalize_pack_quantity(
                normalized["pack_quantity"]
            )
        )

    return normalized