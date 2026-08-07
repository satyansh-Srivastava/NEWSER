"""Generic RSS/Atom fetcher (feedparser) shared by arXiv, TechCrunch,
VentureBeat, and Google News -- any source whose feed is already scoped to
AI content, so no keyword filtering is applied here."""
from __future__ import annotations

import calendar
import logging
import re
from datetime import datetime, timezone

import feedparser

from newser import config
from newser.fetchers.base import Fetcher
from newser.models import NewsItem

logger = logging.getLogger(__name__)

_TAG_RE = re.compile(r"<[^>]+>")


def _clean_html(raw: str) -> str:
    text = _TAG_RE.sub(" ", raw or "")
    text = re.sub(r"\s+", " ", text).strip()
    return text


def _entry_published(entry) -> datetime:
    parsed = entry.get("published_parsed") or entry.get("updated_parsed")
    if parsed:
        return datetime.fromtimestamp(calendar.timegm(parsed), tz=timezone.utc)
    return datetime.now(timezone.utc)


def parse_feed(feed_url: str, source_key: str, source_name: str) -> list[NewsItem]:
    try:
        parsed = feedparser.parse(
            feed_url,
            agent=config.USER_AGENT,
            request_headers={"User-Agent": config.USER_AGENT},
        )
    except Exception as exc:  # feedparser swallows most errors internally
        logger.warning("RSS %s: failed to parse %s: %s", source_name, feed_url, exc)
        return []

    if getattr(parsed, "bozo", False) and not parsed.entries:
        logger.warning(
            "RSS %s: bozo feed with no entries (%s)", source_name, parsed.get("bozo_exception")
        )

    items: list[NewsItem] = []
    for entry in parsed.entries:
        summary_raw = entry.get("summary", "") or entry.get("description", "")
        summary = _clean_html(summary_raw)
        if len(summary) > 300:
            summary = summary[:300] + "..."

        items.append(
            NewsItem(
                title=_clean_html(entry.get("title", "")),
                url=entry.get("link", ""),
                source_key=source_key,
                source_name=source_name,
                published=_entry_published(entry),
                summary=summary,
                author=entry.get("author"),
            )
        )
    return items


class GenericRssFetcher(Fetcher):
    def __init__(self, key: str, name: str, url: str, max_items: int = 10) -> None:
        self.source_key = key
        self.name = name
        self.url = url
        self.max_items = max_items

    def fetch(self) -> list[NewsItem]:
        items = parse_feed(self.url, self.source_key, self.name)
        return items[: self.max_items]
