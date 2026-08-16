import hashlib
import json
import os
from pathlib import Path

from .ai_extractor import GeminiAIExtractor
from .normalizer import normalize_attribute_record
from .attribute_evidence import build_attribute_evidence


CACHE_PATH = Path("data/cache/ai_attributes.json")


class AttributeEnricher:
    """
    Attribute enrichment layer.

    Supports:
    - Gemini AI mode
    - deterministic mock mode
    - persistent JSON cache

    Environment variable:

        AI_MODE=gemini
        AI_MODE=mock
    """

    def __init__(self , extractor = None):

        self.mode = os.getenv("AI_MODE", "gemini").lower()

        self.extractor = extractor or GeminiAIExtractor()

        CACHE_PATH.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        if CACHE_PATH.exists():

            try:
                with open(
                    CACHE_PATH,
                    "r",
                    encoding="utf-8",
                ) as f:
                    self.cache = json.load(f)

            except (json.JSONDecodeError, OSError):

                self.cache = {}

        else:

            self.cache = {}

    def _cache_key(self, text: str) -> str:

        return hashlib.sha256(
            text.strip().encode("utf-8")
        ).hexdigest()

    def _save_cache(self):

        with open(
            CACHE_PATH,
            "w",
            encoding="utf-8",
        ) as f:

            json.dump(
                self.cache,
                f,
                indent=2,
                ensure_ascii=False,
            )

    def _mock_extract(self, text: str) -> dict:

        """
        Deterministic fallback used during tests/demo.

        Important:
        Mock mode must NOT invent attributes.
        """

        text_lower = text.lower()

        result = {
            "diameter": None,
            "thickness": None,
            "arbor": None,
            "length": None,
            "width": None,
            "height": None,
            "pack_quantity": None,
            "product_type": None,
        }

        if "metal cut off" in text_lower:

            result["product_type"] = "Metal Cut Off Disc"

        return result

    def enrich(self, text: str) -> dict:

        key = self._cache_key(text)
        raw_attrs = self.extractor.extract_product_attributes(text)

        from src.normalizer import normalize_attribute_record
        normalized = normalize_attribute_record(raw_attrs)
        return {
            "normalized": normalized,
            "status": "accepted" if normalized else "rejected",
        }

        # -------------------------------------------------
        # 1. CACHE
        # -------------------------------------------------

        if key in self.cache:

            raw = self.cache[key]

        # -------------------------------------------------
        # 2. MOCK MODE
        # -------------------------------------------------

        elif self.mode == "mock":

            raw = self._mock_extract(text)

            self.cache[key] = raw
            self._save_cache()

        # -------------------------------------------------
        # 3. GEMINI MODE
        # -------------------------------------------------

        else:

            raw = self.extractor.extract_product_attributes(
                text
            )

            self.cache[key] = raw
            self._save_cache()

        # -------------------------------------------------
        # 4. NORMALIZATION
        # -------------------------------------------------

        normalized = normalize_attribute_record(raw)

        # -------------------------------------------------
        # 5. EVIDENCE
        # -------------------------------------------------

        evidence = build_attribute_evidence(
            raw,
            normalized,
        )

        # -------------------------------------------------
        # 6. CONFIDENCE
        # -------------------------------------------------

        confidence = {}

        for attribute in normalized:

            if normalized[attribute] is not None:

                confidence[attribute] = 0.85

        # -------------------------------------------------
        # 7. STATUS
        # -------------------------------------------------

        if evidence:

            status = "accepted"

        else:

            status = "needs_review"

        return {
            "raw": raw,
            "normalized": normalized,
            "confidence": confidence,
            "evidence": evidence,
            "status": status,
        }