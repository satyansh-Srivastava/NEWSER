"""Shared data model for a single news item, regardless of source."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone


@dataclass
class NewsItem:
    title: str
    url: str
    source_key: str          # e.g. "hackernews", "reddit_artificial"
    source_name: str         # e.g. "Hacker News", "r/artificial"
    published: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    summary: str = ""        # short snippet/description
    author: str | None = None
    score: int | None = None       # upvotes/points, if the source has them
    comments: int | None = None    # comment count, if the source has them

    @property
    def normalized_title(self) -> str:
        import re
        text = self.title.lower().strip()
        text = re.sub(r"[^a-z0-9\s]", "", text)
        text = re.sub(r"\s+", " ", text)
        return text

    @property
    def published_str(self) -> str:
        return self.published.strftime("%b %d, %H:%M UTC")
