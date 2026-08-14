import re
from typing import Optional


def extract_product_facts(text: str) -> dict:
    """
    Extract obvious technical specifications from retrieved
    manufacturer text.

    This is the deterministic baseline.
    """

    facts = {}

    # Diameter
    diameter = re.search(
        r'(\d+(?:-\d+/\d+)?(?:\.\d+)?)["″]\s*x',
        text,
        re.IGNORECASE,
    )

    if diameter:
        facts["diameter"] = diameter.group(1) + " in"

    # Thickness
    thickness = re.search(
        r'x\s*(\.\d+|\d+(?:\.\d+)?)["″]\s*x',
        text,
        re.IGNORECASE,
    )

    if thickness:
        facts["thickness"] = thickness.group(1) + " in"

    # Arbor
    arbor = re.search(
        r'x\s*(\d+(?:/\d+)?(?:-\d+/\d+)?)["″]',
        text,
        re.IGNORECASE,
    )

    if arbor:
        facts["arbor"] = arbor.group(1) + " in"

    # Type
    type_match = re.search(
        r'Type\s+(\d+)',
        text,
        re.IGNORECASE,
    )

    if type_match:
        facts["wheel_type"] = "Type " + type_match.group(1)

    # RPM
    rpm = re.search(
        r'(\d[\d,]*)\s*(?:RPM|rpm)',
        text,
        re.IGNORECASE,
    )

    if rpm:
        facts["max_rpm"] = rpm.group(1) + " RPM"

    return facts