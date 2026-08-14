from rapidfuzz import process, fuzz
from .master_data import load_manufacturer_brand_master

from .master_data import (
    manufacturer_names,
    brand_names,
)


def resolve_manufacturer(
    candidate: str,
    threshold: int = 75,
) -> dict:

    if not candidate:
        return {
            "value": None,
            "score": 0,
            "match": None,
        }

    names = manufacturer_names()

    result = process.extractOne(
        candidate,
        names,
        scorer=fuzz.token_set_ratio,
    )

    if result is None:
        return {
            "value": None,
            "score": 0,
            "match": None,
        }

    match, score, _ = result

    if score < threshold:
        return {
            "value": None,
            "score": score,
            "match": match,
        }

    return {
        "value": match,
        "score": score,
        "match": match,
    }


def resolve_brand(
    candidate: str,
    threshold: int = 75,
) -> dict:

    if not candidate:
        return {
            "value": None,
            "score": 0,
            "match": None,
        }

    names = brand_names()

    result = process.extractOne(
        candidate,
        names,
        scorer=fuzz.token_set_ratio,
    )

    if result is None:
        return {
            "value": None,
            "score": 0,
            "match": None,
        }

    match, score, _ = result

    if score < threshold:
        return {
            "value": None,
            "score": score,
            "match": match,
        }

    return {
        "value": match,
        "score": score,
        "match": match,
    }
def resolve_brand_for_manufacturer(
    brand_candidate: str,
    manufacturer_candidate: str,
) -> dict:

    df = load_manufacturer_brand_master()

    manufacturer_result = resolve_manufacturer(
        manufacturer_candidate
    )

    canonical_manufacturer = manufacturer_result["value"]

    if not canonical_manufacturer:
        return {
            "brand": None,
            "manufacturer": None,
            "confidence": 0,
            "status": "manufacturer_unresolved",
        }

    subset = df[
        df["MANUFACTURER_NAME"].astype(str).str.strip()
        == canonical_manufacturer
    ]

    if subset.empty:
        return {
            "brand": None,
            "manufacturer": canonical_manufacturer,
            "confidence": 0,
            "status": "no_brand_mapping",
        }

    candidates = (
        subset["BRAND_NAME"]
        .dropna()
        .astype(str)
        .str.strip()
        .unique()
        .tolist()
    )

    result = process.extractOne(
        brand_candidate,
        candidates,
        scorer=fuzz.token_set_ratio,
    )

    if result is None:
        return {
            "brand": None,
            "manufacturer": canonical_manufacturer,
            "confidence": 0,
            "status": "brand_unresolved",
        }

    brand, score, _ = result

    if score < 75:
        return {
            "brand": None,
            "manufacturer": canonical_manufacturer,
            "confidence": score,
            "status": "needs_review",
        }

    return {
        "brand": brand,
        "manufacturer": canonical_manufacturer,
        "confidence": score,
        "status": "resolved",
    }