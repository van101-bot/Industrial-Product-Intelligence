import re
from difflib import SequenceMatcher

from src.lov_profile import LOVProfile


def _normalize_text(value: str) -> str:

    value = str(value or "").lower()

    value = re.sub(
        r"[^a-z0-9]+",
        " ",
        value,
    )

    return " ".join(
        value.split()
    )


def _similarity(a: str, b: str) -> float:

    return SequenceMatcher(
        None,
        _normalize_text(a),
        _normalize_text(b),
    ).ratio()


class LOVEngine:

    def __init__(
        self,
        profile: LOVProfile,
    ):

        self.profile = profile

    # ---------------------------------------------------------
    # TAXONOMY
    # ---------------------------------------------------------

    def classify(
        self,
        description: str,
    ) -> dict:

        description = str(
            description or ""
        ).strip()

        if not description:

            return {
                "category": None,
                "confidence": 0.0,
                "source": "unresolved",
            }

        normalized = _normalize_text(
            description
        )

        best = None
        best_score = 0.0

        for category in self.profile.taxonomy_paths:

            category_words = (
                _normalize_text(category)
                .split()
            )

            if not category_words:
                continue

            matches = sum(
                1
                for word in category_words
                if word in normalized
            )

            keyword_score = (
                matches / len(category_words)
            )

            similarity = _similarity(
                description,
                category,
            )

            score = max(
                keyword_score,
                similarity,
            )

            if score > best_score:

                best_score = score
                best = category

        if best is None:

            return {
                "category": None,
                "confidence": 0.0,
                "source": "lov_unresolved",
            }

        if best_score < 0.55:

            return {
                "category": None,
                "confidence": round(
                    best_score,
                    3,
                ),
                "source": "lov_unresolved",
            }

        return {
            "category": best,
            "confidence": round(
                min(best_score, 0.99),
                3,
            ),
            "source": "company_lov",
        }

    # ---------------------------------------------------------
    # CONTROLLED ATTRIBUTE VALUES
    # ---------------------------------------------------------

    def normalize_attribute(
        self,
        attribute: str,
        value: str,
    ) -> dict:

        if not value:

            return {
                "value": None,
                "confidence": 0.0,
                "source": "empty",
            }

        allowed = self.profile.attribute_values.get(
            attribute,
            [],
        )

        if not allowed:

            return {
                "value": value,
                "confidence": 0.50,
                "source": "uncontrolled",
            }

        # Exact match
        for candidate in allowed:

            if _normalize_text(
                candidate
            ) == _normalize_text(value):

                return {
                    "value": candidate,
                    "confidence": 1.0,
                    "source": "company_lov",
                }

        # Fuzzy match
        best = None
        best_score = 0.0

        for candidate in allowed:

            score = _similarity(
                value,
                candidate,
            )

            if score > best_score:

                best_score = score
                best = candidate

        if best is not None and best_score >= 0.82:

            return {
                "value": best,
                "confidence": round(
                    best_score,
                    3,
                ),
                "source": "company_lov_fuzzy",
            }

        return {
            "value": None,
            "confidence": round(
                best_score,
                3,
            ),
            "source": "lov_unresolved",
        }

    # ---------------------------------------------------------
    # VALIDATION
    # ---------------------------------------------------------

    def validate_attribute(
        self,
        attribute: str,
        value: str,
    ) -> dict:

        allowed = self.profile.attribute_values.get(
            attribute,
            [],
        )

        if not allowed:

            return {
                "valid": True,
                "reason": "attribute_not_controlled",
            }

        normalized_value = _normalize_text(
            value
        )

        for candidate in allowed:

            if (
                _normalize_text(candidate)
                == normalized_value
            ):

                return {
                    "valid": True,
                    "reason": "exact_lov_match",
                }

        return {
            "valid": False,
            "reason": "value_not_in_lov",
        }

    # ---------------------------------------------------------
    # PROFILE
    # ---------------------------------------------------------

    def profile_summary(self):

        return self.profile.summary()