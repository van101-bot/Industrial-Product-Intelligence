from dataclasses import dataclass, asdict
from typing import Any


@dataclass
class EvidenceRecord:

    field: str
    value: Any
    source: str
    confidence: float
    reason: str = ""

    def to_dict(self) -> dict:
        return asdict(self)


def make_evidence(
    field: str,
    value: Any,
    source: str,
    confidence: float,
    reason: str = "",
) -> dict:

    return EvidenceRecord(
        field=field,
        value=value,
        source=source,
        confidence=float(confidence),
        reason=reason,
    ).to_dict()