"""arXiv cs.AI RSS fetcher."""
from __future__ import annotations

import logging

from newser import config
from newser.fetchers.base import Fetcher
from newser.fetchers.rss_feed import parse_feed
from newser.models import NewsItem

logger = logging.getLogger(__name__)


class ArxivFetcher(Fetcher):
    source_key = "arxiv"

    def __init__(
        self,
        feed_url: str = config.ARXIV_RSS_URL,
        max_items: int = config.ARXIV_MAX_ITEMS,
    ) -> None:
        self.feed_url = feed_url
        self.max_items = max_items

    def fetch(self) -> list[NewsItem]:
        source_name = config.SECTION_META[self.source_key]["name"]
        items = parse_feed(self.feed_url, self.source_key, source_name)
        return items[: self.max_items]
