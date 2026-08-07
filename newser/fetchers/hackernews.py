"""Hacker News fetcher, using the official Firebase API.

The API has no topic filter, so we scan the current top stories and keep
only the ones whose titles look AI-related (see newser.filters.is_ai_related).
"""
from __future__ import annotations

import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone

import requests

from newser import config
from newser.fetchers.base import Fetcher
from newser.filters import is_ai_related
from newser.models import NewsItem

logger = logging.getLogger(__name__)


class HackerNewsFetcher(Fetcher):
    source_key = "hackernews"

    def __init__(
        self,
        stories_to_scan: int = config.HN_STORIES_TO_SCAN,
        max_items: int = config.HN_MAX_ITEMS,
    ) -> None:
        self.stories_to_scan = stories_to_scan
        self.max_items = max_items

    def fetch(self) -> list[NewsItem]:
        try:
            resp = requests.get(
                config.HN_TOP_STORIES_URL,
                headers={"User-Agent": config.USER_AGENT},
                timeout=config.REQUEST_TIMEOUT_SECONDS,
            )
            resp.raise_for_status()
            story_ids = resp.json()[: self.stories_to_scan]
        except (requests.RequestException, ValueError) as exc:
            logger.warning("HackerNews: failed to fetch top stories: %s", exc)
            return []

        items: list[NewsItem] = []
        with ThreadPoolExecutor(max_workers=16) as pool:
            futures = {pool.submit(self._fetch_item, sid): sid for sid in story_ids}
            for future in as_completed(futures):
                item = future.result()
                if item is not None:
                    items.append(item)

        items.sort(key=lambda i: i.score or 0, reverse=True)
        return items[: self.max_items]

    def _fetch_item(self, story_id: int) -> NewsItem | None:
        try:
            resp = requests.get(
                config.HN_ITEM_URL.format(id=story_id),
                headers={"User-Agent": config.USER_AGENT},
                timeout=config.REQUEST_TIMEOUT_SECONDS,
            )
            resp.raise_for_status()
            data = resp.json()
        except (requests.RequestException, ValueError) as exc:
            logger.debug("HackerNews: failed to fetch item %s: %s", story_id, exc)
            return None

        if not data or data.get("type") != "story":
            return None

        title = data.get("title", "")
        if not is_ai_related(title):
            return None

        discussion_url = f"https://news.ycombinator.com/item?id={story_id}"
        return NewsItem(
            title=title,
            url=data.get("url") or discussion_url,
            source_key=self.source_key,
            source_name=config.SECTION_META[self.source_key]["name"],
            published=datetime.fromtimestamp(data.get("time", 0), tz=timezone.utc),
            summary=f"Discussion: {discussion_url}",
            author=data.get("by"),
            score=data.get("score"),
            comments=data.get("descendants"),
        )
