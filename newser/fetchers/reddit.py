"""Reddit fetcher using the public .json listing endpoints (no OAuth needed)."""
from __future__ import annotations

import logging
from datetime import datetime, timezone

import requests

from newser import config
from newser.fetchers.base import Fetcher
from newser.models import NewsItem

logger = logging.getLogger(__name__)


class RedditFetcher(Fetcher):
    def __init__(
        self,
        subreddit: str,
        listing: str = config.REDDIT_LISTING,
        limit: int = config.REDDIT_LIMIT,
        max_items: int = config.REDDIT_MAX_ITEMS_PER_SUB,
    ) -> None:
        self.subreddit = subreddit
        self.listing = listing
        self.limit = limit
        self.max_items = max_items
        self.source_key = f"reddit_{subreddit.lower()}"

    def fetch(self) -> list[NewsItem]:
        url = f"https://www.reddit.com/r/{self.subreddit}/{self.listing}.json"
        try:
            resp = requests.get(
                url,
                params={"limit": self.limit},
                headers={"User-Agent": config.USER_AGENT},
                timeout=config.REQUEST_TIMEOUT_SECONDS,
            )
            resp.raise_for_status()
            payload = resp.json()
        except (requests.RequestException, ValueError) as exc:
            logger.warning("Reddit r/%s: failed to fetch: %s", self.subreddit, exc)
            return []

        children = payload.get("data", {}).get("children", [])
        source_name = config.SECTION_META.get(
            self.source_key, {"name": f"r/{self.subreddit}"}
        )["name"]

        items: list[NewsItem] = []
        for child in children:
            post = child.get("data", {})
            if post.get("stickied"):
                continue

            permalink = f"https://reddit.com{post.get('permalink', '')}"
            external_url = post.get("url") or permalink
            selftext = (post.get("selftext") or "").strip()
            summary = (selftext[:300] + "...") if len(selftext) > 300 else selftext
            if not summary and not post.get("is_self"):
                summary = f"Link post -> {external_url}"

            items.append(
                NewsItem(
                    title=post.get("title", ""),
                    url=external_url,
                    source_key=self.source_key,
                    source_name=source_name,
                    published=datetime.fromtimestamp(
                        post.get("created_utc", 0), tz=timezone.utc
                    ),
                    summary=summary,
                    author=post.get("author"),
                    score=post.get("score"),
                    comments=post.get("num_comments"),
                )
            )

        items.sort(key=lambda i: i.score or 0, reverse=True)
        return items[: self.max_items]
