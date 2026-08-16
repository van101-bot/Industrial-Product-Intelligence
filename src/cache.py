import hashlib
import json
from pathlib import Path


CACHE_DIR = Path("data/cache")


def _key(text: str) -> str:

    return hashlib.sha256(
        text.strip().encode("utf-8")
    ).hexdigest()


def get_cached(text: str):

    CACHE_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    path = CACHE_DIR / f"{_key(text)}.json"

    if not path.exists():
        return None

    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_cached(text: str, result: dict):

    CACHE_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    path = CACHE_DIR / f"{_key(text)}.json"

    with open(
        path,
        "w",
        encoding="utf-8",
    ) as f:

        json.dump(
            result,
            f,
            indent=2,
        )