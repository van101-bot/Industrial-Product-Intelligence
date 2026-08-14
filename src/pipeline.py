from .cleaner import clean_product_row
from .identity import build_identity
from .brand_resolver import resolve_brand
from .entity_resolver import (
    resolve_manufacturer,
    resolve_brand_for_manufacturer,
)


def enrich_product(row) -> dict:

    cleaned = clean_product_row(row)

    identity = build_identity(cleaned)

    brand_result = resolve_brand(cleaned)

    manufacturer_result = resolve_manufacturer(
        identity.get("manufacturer_candidate")
    )

    resolved_identity = resolve_brand_for_manufacturer(
        brand_result.get("brand"),
        identity.get("manufacturer_candidate"),
    )

    return {
        "identity": identity,

        "brand_detection": brand_result,

        "manufacturer_resolution": manufacturer_result,

        "canonical_identity": resolved_identity,

        "input": cleaned,
    }