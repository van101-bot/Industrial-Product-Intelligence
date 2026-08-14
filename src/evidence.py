from dataclasses import dataclass
from typing import Optional


@dataclass
class Evidence:
    field: str
    value: str
    source_url: str
    source_type: str
    confidence: float
    excerpt: Optional[str] = None

    def to_dict(self) -> dict:
        return {
            "field": self.field,
            "value": self.value,
            "source_url": self.source_url,
            "source_type": self.source_type,
            "confidence": self.confidence,
            "excerpt": self.excerpt,
        }