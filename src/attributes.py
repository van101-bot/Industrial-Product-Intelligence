import re

from .ai_extractor import GeminiAIExtractor
from .normalizer import normalize_attribute_record
from .attribute_evidence import build_attribute_evidence
from .fallback_attributes import extract_attributes_fallback


class AttributeEnricher:

    def __init__(self, extractor=None, use_ai=True):

        self.use_ai = use_ai

        if extractor is not None:
            self.extractor = extractor
        else:
            self.extractor = GeminiAIExtractor()

    def enrich(self, text: str) -> dict:

        raw = None
        source = None

        # Explicitly requested deterministic mode
        if not self.use_ai:

            raw = extract_attributes_fallback(text)
            source = "deterministic_fallback"

        else:

            try:
                raw = self.extractor.extract_product_attributes(text)
                source = "ai_extraction"

            except Exception:

                raw = extract_attributes_fallback(text)
                source = "deterministic_fallback"

        normalized = normalize_attribute_record(raw)

        evidence = build_attribute_evidence(
            raw,
            normalized,
        )

        confidence = {}

        for attribute, value in normalized.items():

            if value is not None:

                if source == "ai_extraction":
                    confidence[attribute] = 0.85
                else:
                    confidence[attribute] = 0.70

        return {
            "raw": raw,
            "normalized": normalized,
            "confidence": confidence,
            "evidence": evidence,
            "status": "accepted",
        }

def extract_pack_quantity(text: str):

    match = re.search(
        r"\b(\d+)\s*(?:pc|pcs|piece|pieces|pack|pk|/box)\b",
        text,
        re.IGNORECASE,
    )

    if match:
        return int(match.group(1))

    return None


def extract_dimensions(text: str):

    normalized = text.replace("×", "x")

    pattern = (
        r'(\d+(?:\.\d+)?(?:/\d+)?)\s*"'
        r'\s*x\s*'
        r'(\d+(?:\.\d+)?(?:/\d+)?)\s*"'
    )

    match = re.search(
        pattern,
        normalized,
        re.IGNORECASE,
    )

    if not match:
        return {}

    return {
        "dimension_1": match.group(1),
        "dimension_2": match.group(2),
    }