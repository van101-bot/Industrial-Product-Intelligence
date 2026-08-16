import re


def extract_attributes_fallback(text: str) -> dict:
    """
    Deterministic attribute extraction used when Gemini
    is unavailable.
    """

    text = text or ""

    result = {
        "diameter": None,
        "thickness": None,
        "arbor": None,
        "product_type": None,
        "pack_quantity": None,
    }

    # Example:
    # 4-1/2"x.045"x7/8"
    dimension_pattern = re.search(
        r'(\d+(?:-\d+/\d+)?|\d+/\d+)"?\s*x\s*'
        r'(\.?\d+(?:-\d+/\d+)?)"?\s*x\s*'
        r'(\d+(?:-\d+/\d+)?)',
        text,
        re.IGNORECASE,
    )

    if dimension_pattern:

        result["diameter"] = dimension_pattern.group(1)
        result["thickness"] = dimension_pattern.group(2)
        result["arbor"] = dimension_pattern.group(3)

    # Product type
    lowered = text.lower()

    if "cut off disc" in lowered:
        result["product_type"] = "Metal Cut Off Disc"

    elif "cut-off disc" in lowered:
        result["product_type"] = "Metal Cut Off Disc"

    elif "sanding belt" in lowered:
        result["product_type"] = "Sanding Belt"

    elif "sanding disc" in lowered:
        result["product_type"] = "Sanding Disc"

    # Pack quantity
    pack_match = re.search(
        r'(\d+)\s*(?:pc|pcs|piece|pieces|disc/box)',
        text,
        re.IGNORECASE,
    )

    if pack_match:
        result["pack_quantity"] = int(pack_match.group(1))

    return result