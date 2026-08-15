from .ai_extractor import GeminiAIExtractor
from .normalizer import normalize_attribute_record


class AttributeEnricher:
    """
    Deterministic attribute enrichment layer.

    Automated tests use MockAIExtractor so tests do not depend
    on Gemini API availability.
    """

    def __init__(self):

        self.extractor = GeminiAIExtractor()

    def enrich(self, text: str) -> dict:

        raw = self.extractor.extract_product_attributes(text)

        normalized = normalize_attribute_record(raw)

        return {
            "raw": raw,
            "normalized": normalized,
        }
    