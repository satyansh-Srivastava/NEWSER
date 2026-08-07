"""Twitter/X fetcher -- STUBBED, disabled by default.

Fetching curated lists requires a paid X API tier (list timeline endpoints
are not available on the free tier). This class exists so the harness has
a stable extension point: once you have API access, implement `fetch()`
using the `tweepy` client or direct calls to
`GET /2/lists/:id/tweets`, and flip `config.ENABLE_TWITTER = True`.
"""
from __future__ import annotations

import logging

from newser.fetchers.base import Fetcher
from newser.models import NewsItem

logger = logging.getLogger(__name__)


class TwitterFetcher(Fetcher):
    source_key = "twitter"

    def __init__(self, list_ids: list[str] | None = None) -> None:
        self.list_ids = list_ids or []

    def fetch(self) -> list[NewsItem]:
        logger.info("Twitter/X fetcher is disabled (requires paid API access); skipping.")
        return []
