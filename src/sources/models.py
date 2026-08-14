from dataclasses import dataclass
from typing import Optional


@dataclass
class SearchResult:
    title: str
    url: str
    snippet: str
    domain: str
    source_type: str = "unknown"
    score: float = 0.0
    reason: Optional[str] = None

    def to_dict(self) -> dict:
        return {
            "title": self.title,
            "url": self.url,
            "snippet": self.snippet,
            "domain": self.domain,
            "source_type": self.source_type,
            "score": self.score,
            "reason": self.reason,
        }