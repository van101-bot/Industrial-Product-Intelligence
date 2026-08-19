import re

TAXONOMY_RULES = [
    # ---------------------------------------------------------
    # ABRASIVES
    # ---------------------------------------------------------
    (
        "Abrasives > Cut-Off Discs",
        [r"\bcut[\s-]*off\b", r"\bcutoff\b"],
    ),
    (
        "Abrasives > Cut & Grind Discs",
        [r"\bcut\s+and\s+grind\b", r"\bcut\s+n\s+grind\b", r"\bcut\s*&\s*grind\b", r"\bdual\s+metal\s+cut\b"],
    ),
    (
        "Abrasives > Grinding Wheels",
        [r"\bgrinding wheel\b", r"\bgrinding wheels\b"],
    ),
    (
        "Abrasives > Sanding Belts",
        [r"\bsanding belt\b", r"\bsanding belts\b"],
    ),
    (
        "Abrasives > Sanding Discs",
        [r"\bsanding disc\b", r"\bsanding discs\b"],
    ),
    (
        "Abrasives > Sanding Sponges",
        [r"\bsanding sponge\b", r"\bsanding sponges\b"],
    ),
    (
        "Abrasives > Abrasive Sheets",
        [r"\babrasive sheet\b", r"\babrasive sheets\b", r"\bsanding sheet\b", r"\bsanding sheets\b"],
    ),
    (
        "Abrasives > Abrasive Rolls",
        [r"\babrasive roll\b", r"\babrasive rolls\b"],
    ),
    (
        "Abrasives > Abrasive Materials",
        [r"\babrasive\b", r"\bhiolit\b", r"\babranet\b", r"\bcubitron\b"],
    ),

    # ---------------------------------------------------------
    # TAPES
    # ---------------------------------------------------------
    (
        "Tapes > Electrical Tape",
        [r"\belect(?:rical)?\s+tape\b", r"\belect\s+tape\b"],
    ),
    (
        "Tapes",
        [r"\btape\b"],
    ),

    # ---------------------------------------------------------
    # APPLIANCES
    # ---------------------------------------------------------
    (
        "Appliances > Dishwashers",
        [r"\bdishwasher\b", r"\bdishwashers\b"],
    ),
    (
        "Appliances > Dryers",
        [r"\bdryer\b", r"\bdryers\b"],
    ),

    # ---------------------------------------------------------
    # HEATING
    # ---------------------------------------------------------
    (
        "Heating > Heater Kits",
        [r"\bheater kit\b", r"\bheater kits\b"],
    ),

    # ---------------------------------------------------------
    # BUILDING MATERIALS
    # ---------------------------------------------------------
    (
        "Building Materials > Decking",
        [r"\bdecking\b"],
    ),
    (
        "Building Materials > Rail Kits",
        [r"\brail kit\b", r"\bt-rail\b"],
    ),

    # ---------------------------------------------------------
    # AUTOMOTIVE
    # ---------------------------------------------------------
    (
        "Automotive > Tire Pressure Gauges",
        [r"\btire pressure\b.*\bgauge\b", r"\bgauge\b.*\btire pressure\b"],
    ),
]


def classify_product(description: str = None, product_type: str = None) -> dict:
    """
    Classify a product description into a taxonomy category.
    Returns a dict with 'category', 'source', and 'confidence'.
    """

    description = description or ""
    product_type = product_type or ""
    text = f"{description} {product_type}".lower()

    for category, patterns in TAXONOMY_RULES:
        for pattern in patterns:
            if re.search(pattern, text, re.IGNORECASE):
                return {
                    "category": category,
                    "source": "rule",
                    "confidence": 0.95,
                }

    return {
        "category": None,
        "source": None,
        "confidence": 0.0,
    }
