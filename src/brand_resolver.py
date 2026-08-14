import re
from typing import Any


PLACEHOLDERS = {
    "-- unbranded --",
    "-- no unilog brand --",
    "-- no dib brand --",
    "",
    None,
}


def normalize_text(value: Any) -> str:
    if value is None:
        return ""

    return re.sub(r"\s+", " ", str(value)).strip()


def is_placeholder(value: Any) -> bool:
    normalized = normalize_text(value).lower()
    return normalized in PLACEHOLDERS


def extract_brand_candidates(description: str) -> list[str]:
    """
    Extract likely brand candidates from a product description.

    This is intentionally conservative.
    It does not claim a candidate is canonical yet.
    """

    description = normalize_text(description)

    if not description:
        return []

    candidates = []

    # Known brand signals observed in the supplied catalogue.
    known_brands = [
        "Diablo",
        "3M",
        "Mirka",
        "Milwaukee",
        "DEWALT",
        "Leviton",
        "Philips",
        "Southwire",
    ]

    for brand in known_brands:
        if re.search(
            rf"(?<![A-Za-z0-9]){re.escape(brand)}(?![A-Za-z0-9])",
            description,
            flags=re.IGNORECASE,
        ):
            candidates.append(brand)

    return candidates


def resolve_brand(row: dict[str, Any]) -> dict[str, Any]:

    description = normalize_text(
        row.get("part_description", "")
    )

    structured_brands = []

    for field in (
        "e1_brand",
        "unilog_brand",
        "dib_brand",
    ):
        value = row.get(field)

        if not is_placeholder(value):
            structured_brands.append(normalize_text(value))

    description_candidates = extract_brand_candidates(description)

    # Prefer explicitly supplied structured brand data.
    if structured_brands:
        return {
            "brand": structured_brands[0],
            "source": "structured_field",
            "confidence": 0.99,
            "candidates": structured_brands,
        }

    # Otherwise expose description-derived candidates as candidates,
    # not as unquestionable truth.
    if description_candidates:
        return {
            "brand": description_candidates[0],
            "source": "description",
            "confidence": 0.85,
            "candidates": description_candidates,
        }

    return {
        "brand": None,
        "source": None,
        "confidence": 0.0,
        "candidates": [],
    }