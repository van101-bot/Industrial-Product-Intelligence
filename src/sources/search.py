from dataclasses import dataclass
from typing import Protocol

from src.sources.models import SearchResult


class SearchProvider(Protocol):

    def search(
        self,
        query: str,
        max_results: int = 10,
    ) -> list[SearchResult]:
        ...


@dataclass
class MockSearchProvider:

    results: list[SearchResult]

    def search(
        self,
        query: str,
        max_results: int = 10,
    ) -> list[SearchResult]:

        return self.results[:max_results]