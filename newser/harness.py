"""The agent harness: runs every fetcher concurrently, filters/dedupes the
results, and groups them into sections ready for rendering."""
from __future__ import annotations

import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from datetime import datetime, timezone

from newser import config
from newser.fetchers.arxiv_rss import ArxivFetcher
from newser.fetchers.base import Fetcher
from newser.fetchers.hackernews import HackerNewsFetcher
from newser.fetchers.reddit import RedditFetcher
from newser.fetchers.rss_feed import GenericRssFetcher
from newser.fetchers.twitter import TwitterFetcher
from newser.filters import dedupe
from newser.models import NewsItem

logger = logging.getLogger(__name__)


@dataclass
class Section:
    key: str
    name: str
    icon: str
    color: str
    items: list[NewsItem]


@dataclass
class Digest:
    generated_at: datetime
    sections: list[Section]

    @property
    def total_items(self) -> int:
        return sum(len(s.items) for s in self.sections)

    @property
    def source_count(self) -> int:
        return len(self.sections)


def build_fetchers(enabled_sources: set[str] | None = None) -> list[Fetcher]:
    """Construct one fetcher per configured source. `enabled_sources`, if
    given, restricts the run to those source_keys (used by --sources)."""
    fetchers: list[Fetcher] = [
        HackerNewsFetcher(),
        RedditFetcher("artificial"),
        RedditFetcher("MachineLearning"),
        ArxivFetcher(),
    ]
    for feed in config.RSS_FEEDS:
        fetchers.append(
            GenericRssFetcher(feed["key"], feed["name"], feed["url"], feed.get("max_items", 10))
        )
    if config.ENABLE_TWITTER:
        fetchers.append(TwitterFetcher())

    if enabled_sources is not None:
        fetchers = [f for f in fetchers if f.source_key in enabled_sources]
    return fetchers


def build_digest(
    enabled_sources: set[str] | None = None,
    max_per_source: int | None = None,
) -> Digest:
    fetchers = build_fetchers(enabled_sources)
    ordered_keys = [f.source_key for f in fetchers]

    results: dict[str, list[NewsItem]] = {}
    with ThreadPoolExecutor(max_workers=max(len(fetchers), 1)) as pool:
        future_to_key = {pool.submit(f.fetch): f.source_key for f in fetchers}
        for future in as_completed(future_to_key):
            key = future_to_key[future]
            try:
                results[key] = future.result()
            except Exception as exc:  # a single bad fetcher shouldn't sink the run
                logger.warning("Fetcher %s raised unexpectedly: %s", key, exc)
                results[key] = []

    # Flatten in a stable priority order, then dedupe across sources so
    # syndicated aggregators (Google News) yield to the original source
    # when the same story appears twice.
    all_items: list[NewsItem] = []
    for key in ordered_keys:
        all_items.extend(results.get(key, []))
    deduped_items = dedupe(all_items)

    items_by_key: dict[str, list[NewsItem]] = {key: [] for key in ordered_keys}
    for item in deduped_items:
        items_by_key[item.source_key].append(item)

    sections: list[Section] = []
    for key in ordered_keys:
        items = items_by_key.get(key, [])
        if max_per_source is not None:
            items = items[:max_per_source]
        if not items:
            continue
        meta = config.SECTION_META.get(
            key, {"name": key, "icon": "\U0001F4C1", "color": "#666666"}
        )
        sections.append(
            Section(key=key, name=meta["name"], icon=meta["icon"], color=meta["color"], items=items)
        )

    return Digest(generated_at=datetime.now(timezone.utc), sections=sections)
