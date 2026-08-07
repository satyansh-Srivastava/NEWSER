"""Relevance filtering and cross-source deduplication."""
from __future__ import annotations

import re

from newser import config
from newser.models import NewsItem

_KEYWORD_PATTERNS = [
    re.compile(r"\b" + re.escape(keyword) + r"\b", re.IGNORECASE)
    for keyword in config.AI_KEYWORDS
]


def is_ai_related(title: str) -> bool:
    """Whether a title looks AI-related, based on config.AI_KEYWORDS."""
    return any(pattern.search(title) for pattern in _KEYWORD_PATTERNS)


def dedupe(items: list[NewsItem]) -> list[NewsItem]:
    """Drop items whose normalized title we've already seen, keeping the
    first (i.e. earliest-fetched-source) occurrence. Source fetch order in
    the harness is used to prefer primary sources over syndicated
    reposts (e.g. Google News re-surfacing a TechCrunch headline)."""
    seen: set[str] = set()
    deduped: list[NewsItem] = []
    for item in items:
        key = item.normalized_title
        if key and key in seen:
            continue
        seen.add(key)
        deduped.append(item)
    return deduped
