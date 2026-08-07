"""Common interface every source fetcher implements."""
from __future__ import annotations

from abc import ABC, abstractmethod

from newser.models import NewsItem


class Fetcher(ABC):
    """A Fetcher knows how to pull items from exactly one source."""

    #: Stable key used for grouping/config (e.g. "hackernews").
    source_key: str = "unknown"

    @abstractmethod
    def fetch(self) -> list[NewsItem]:
        """Return the day's items for this source. Must not raise on
        expected failure modes (network errors, empty feeds) -- log and
        return an empty list instead, so one bad source doesn't take down
        the whole digest."""
        raise NotImplementedError
