from .ai_extractor import GeminiAIExtractor
from .normalizer import normalize_attribute_record
from .attribute_evidence import build_attribute_evidence    


class AttributeEnricher:
    """
    AI-assisted product attribute enrichment.

    Gemini extracts candidate attributes.
    Python deterministically normalizes them.
    """

    def __init__(self, extractor=None):
        self.extractor = extractor or GeminiAIExtractor()

    def enrich(self, text: str) -> dict:
        if not text:
            return {
                "raw": {},
                "normalized": {},
                "confidence": {},
                "evidence": [],
                "status": "needs_review",
            }

        raw = self.extractor.extract_product_attributes(text)

        if not isinstance(raw, dict):
            raw = {}

        normalized = normalize_attribute_record(raw)

        confidence = self._calculate_confidence(
            raw,
            normalized,
        )

        evidence = build_attribute_evidence(
            raw,
            normalized,
        )

        status = self._calculate_status(
            normalized,
            confidence,
        )

        return {
            "raw": raw,
            "normalized": normalized,
            "confidence": confidence,
            "evidence": evidence,
            "status": status,
        }

    @staticmethod
    def _calculate_confidence(raw, normalized):
        """
        Conservative deterministic confidence.

        We do NOT claim that Gemini is correct merely because
        it returned a value.
        """

        confidence = {}

        for field, value in normalized.items():

            if value is None:
                continue

            # Explicitly extracted and successfully normalized.
            if field in raw and raw[field] is not None:
                confidence[field] = 0.85
            else:
                confidence[field] = 0.0

        return confidence

    @staticmethod
    def _calculate_status(normalized, confidence):
        """
        Decide whether the attribute record is usable or
        requires human review.
        """

        if not normalized:
            return "needs_review"

        usable_values = [
            value
            for value in normalized.values()
            if value is not None
        ]

        if not usable_values:
            return "needs_review"

        confident_values = [
            score
            for score in confidence.values()
            if score >= 0.80
        ]

        if confident_values:
            return "accepted"

        return "needs_review"