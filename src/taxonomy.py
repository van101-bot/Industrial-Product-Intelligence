from pathlib import Path
import pandas as pd
import re


INPUT_FILE = "Unihack_ Sample Dataset - Input.csv"


def _find_input_file() -> Path:
    matches = list(Path("data").rglob(INPUT_FILE))

    if matches:
        return matches[0]

    raise FileNotFoundError(
        f"Could not find '{INPUT_FILE}' under data/"
    )


def load_lov() -> pd.DataFrame:
    """
    Load the supplied catalogue data.

    The competition resources available to this project do not
    provide the separate LOV workbook, so taxonomy classification
    is intentionally conservative and description-driven.
    """

    path = _find_input_file()

    df = pd.read_csv(path)

    df.columns = [
        str(column).strip()
        for column in df.columns
    ]

    return df


def get_product_descriptions() -> list[str]:
    df = load_lov()

    return (
        df["Part_Desc"]
        .dropna()
        .astype(str)
        .str.strip()
        .tolist()
    )


def get_manufacturers() -> list[str]:
    df = load_lov()

    return (
        df["Part_Manuf"]
        .dropna()
        .astype(str)
        .str.strip()
        .unique()
        .tolist()
    )


def get_brands() -> list[str]:
    df = load_lov()

    values = []

    for column in [
        "E1_Brand",
        "Unilog_Brand",
        "DIB_Brand",
    ]:
        if column in df.columns:
            values.extend(
                df[column]
                .dropna()
                .astype(str)
                .str.strip()
                .tolist()
            )

    return sorted(set(values))

(
    "Building Materials > Decking",
    [
        r"\bdecking\b",
        r"\bpvc\s+deck\b",
        r"\bazek\b.*\bdeck",
    ],
),

(
    "Building Materials > Rail Kits",
    [
        r"\brail\s+kit\b",
        r"\bfl\s+rail\b",
        r"\bt[- ]?rail\b",
        r"\brail\s+panel\b",
        r"\brail\b.*\bbaluster",
    ],
),

(
    "Building Materials > Gates",
    [
        r"\bgate\b",
    ],
),

(
    "Appliances > Washers",
    [
        r"\bwasher\b",
        r"\bwashing\s+machine\b",
        r"\bsq\s+washer\b",
    ],
),

(
    "Appliances > Dryers",
    [
        r"\bdryer\b",
        r"\belect\s+dryer\b",
    ],
),

(
    "Automotive > Tire Pressure Gauges",
    [
        r"\btire\s+pressure\b",
        r"\btyre\s+pressure\b",
        r"\binflator\s+gauge\b",
    ],
),

(
    "Masonry > Mortar",
    [
        r"\bmortar\b",
        r"\btype\s+[ns]\b.*\bmortar\b",
    ],
),
# ------------------------------------------------------------------
# TAXONOMY
# ------------------------------------------------------------------

TAXONOMY_RULES = [
    (
        "Abrasives > Cut & Grind Discs",
        [
            r"\bcut\s*(?:and|&|n)\s*grind\b",
            r"\bcut\s*and\s*grind\b",
        ],
    ),

    (
        "Abrasives > Cut-Off Discs",
        [
            r"\bcut[- ]?off\b",
            r"\bcutoff\b",
            r"\bcut\s*off\s+disc\b",
        ],
    ),

    (
        "Abrasives > Grinding Wheels",
        [
            r"\bgrinding\s+wheel\b",
            r"\bgrind(?:ing)?\s+wheel\b",
        ],
    ),

    (
        "Abrasives > Sanding Belts",
        [
            r"\bsanding\s+belt\b",
            r"\bsand(?:ing)?\s+belt\b",
        ],
    ),

    (
        "Abrasives > Sanding Sponges",
        [
            r"\bsanding\s+sponge\b",
            r"\bsanding\s+sponges\b",
        ],
    ),

    (
        "Abrasives > Abrasive Materials",
        [
            r"\bcubitron\b",
            r"\bstikit\b",
            r"\bhiolit\b",
            r"\babranet\b",
            r"\babrasive\b",
            r"\bsandpaper\b",
            r"\bsanding\s+disc\b",
            r"\bsanding\s+sheet\b",
            r"\bsanding\s+film\b",
        ],
    ),

    (
        "Appliances > Dishwashers",
        [
            r"\bdishwasher\b",
        ],
    ),

    (
        "Appliances > Dryers",
        [
            r"\bdryer\b",
            r"\belect\s+dryer\b",
        ],
    ),

    (
        "Appliances > Washers",
        [
            r"\bwasher\b",
            r"\bwashing\s+machine\b",
        ],
    ),

    (
        "Tapes > Electrical Tape",
        [
            r"\belect(?:rical)?\s+tape\b",
        ],
    ),

    (
        "Tapes",
        [
            r"\btape\b",
        ],
    ),

    (
        "Heating > Heater Kits",
        [
            r"\bheater\s+kit\b",
            r"\bheating\s+kit\b",
        ],
    ),

    (
        "Masonry > Mortar",
        [
            r"\bmortar\b",
        ],
    ),

    (
        "Automotive > Tire Pressure Gauges",
        [
            r"\btire\s+pressure\b",
            r"\btyre\s+pressure\b",
        ],
    ),

    (
        "Building Materials > Rail Kits",
        [
            r"\brail\s+kit\b",
            r"\brailing\b",
            r"\brail\s+panel\b",
        ],
    ),

    (
        "Building Materials > Gates",
        [
            r"\bgate\b",
        ],
    ),
]

def classify_description(text: str) -> dict:

    text = str(text or "").strip()

    if not text:
        return {
            "taxonomy": None,
            "taxonomy_confidence": 0.0,
        }

    normalized = re.sub(
        r"\s+",
        " ",
        text.lower()
    )

    for taxonomy, patterns in TAXONOMY_RULES:

        for pattern in patterns:

            if re.search(pattern, normalized):

                pattern_length = len(pattern)

                if pattern_length >= 30:
                    confidence = 0.95
                elif pattern_length >= 15:
                    confidence = 0.90
                else:
                    confidence = 0.82

                return {
                    "taxonomy": taxonomy,
                    "taxonomy_confidence": confidence,
                }

    return {
        "taxonomy": None,
        "taxonomy_confidence": 0.0,
    }


def classify_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add taxonomy and taxonomy_confidence columns.

    Classification is based directly on Part_Desc rather than
    requiring product_type to exist.
    """

    result = df.copy()

    classifications = result["Part_Desc"].apply(
        classify_description
    )

    result["taxonomy"] = classifications.apply(
        lambda x: x["taxonomy"]
    )

    result["taxonomy_confidence"] = classifications.apply(
        lambda x: x["taxonomy_confidence"]
    )

    return result