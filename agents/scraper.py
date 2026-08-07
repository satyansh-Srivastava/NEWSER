"""Scraper Agent -- polls Hacker News + Reddit, applies the qualification
thresholds from config.yaml, and outputs qualified_posts.json. Only
qualifying items are kept; full body text is fetched later by the
Extractor Agent so we don't spend bandwidth on posts that don't qualify.
"""
from __future__ import annotations

import json
import logging
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path

import requests

from agents.config import Config
from agents.issue_log import record_issue
from agents.models import QualifiedPost, dump_json

logger = logging.getLogger(__name__)

USER_AGENT = "glueball-agent/0.1 (+https://github.com/satyansh-Srivastava/newser)"
REQUEST_TIMEOUT = 10

HN_TOP_STORIES_URL = "https://hacker-news.firebaseio.com/v0/topstories.json"
HN_ITEM_URL = "https://hacker-news.firebaseio.com/v0/item/{id}.json"
HN_STORIES_TO_SCAN = 200

MAX_429_RETRIES = 3
RETRY_BACKOFF_SECONDS = 60


def qualify_hn_post(score, threshold: int) -> bool:
    if not isinstance(score, (int, float)):
        return False
    return score >= threshold


def qualify_reddit_post(upvotes, comments, ratio: float) -> bool:
    if not isinstance(upvotes, (int, float)) or not isinstance(comments, (int, float)):
        return False
    return upvotes / max(comments, 1) >= ratio


def _get_with_retry(session, url, *, params=None, sleep=time.sleep, max_retries=MAX_429_RETRIES):
    """GET with the spec's 429 handling: pause 60s and retry, up to
    max_retries times, then raise so the caller can mark the source
    unreachable."""
    attempt = 0
    while True:
        resp = session.get(url, params=params, headers={"User-Agent": USER_AGENT}, timeout=REQUEST_TIMEOUT)
        if resp.status_code == 429:
            attempt += 1
            if attempt > max_retries:
                resp.raise_for_status()
            sleep(RETRY_BACKOFF_SECONDS)
            continue
        resp.raise_for_status()
        return resp


def fetch_hackernews(config: Config, *, session=requests, sleep=time.sleep) -> tuple[list[QualifiedPost], bool]:
    """Returns (qualified_posts, source_reachable)."""
    try:
        resp = _get_with_retry(session, HN_TOP_STORIES_URL, sleep=sleep)
        story_ids = resp.json()[:HN_STORIES_TO_SCAN]
    except Exception as exc:
        record_issue("scraper.hackernews", f"Error - Unreachable: {exc}")
        return [], False

    posts: list[QualifiedPost] = []

    def fetch_item(story_id):
        try:
            r = _get_with_retry(session, HN_ITEM_URL.format(id=story_id), sleep=sleep)
            return r.json()
        except Exception as exc:
            record_issue("scraper.hackernews", f"failed to fetch item {story_id}: {exc}", item_id=str(story_id))
            return None

    with ThreadPoolExecutor(max_workers=16) as pool:
        futures = [pool.submit(fetch_item, sid) for sid in story_ids]
        for future in as_completed(futures):
            item = future.result()
            if not item or item.get("type") != "story":
                continue

            score = item.get("score")
            if score is None:
                record_issue(
                    "scraper.hackernews",
                    "missing score field, dropping post",
                    item_id=str(item.get("id")),
                )
                continue

            if not qualify_hn_post(score, config.hn_threshold):
                continue

            story_id = item["id"]
            posts.append(
                QualifiedPost(
                    id=str(story_id),
                    source="hackernews",
                    title=item.get("title", ""),
                    url=item.get("url") or f"https://news.ycombinator.com/item?id={story_id}",
                    score=score,
                    comments=item.get("descendants", 0) or 0,
                    subreddit=None,
                    qualified_at=datetime.now(timezone.utc).isoformat(),
                )
            )

    return posts, True


def fetch_reddit(config: Config, *, session=requests, sleep=time.sleep) -> tuple[list[QualifiedPost], bool]:
    """Returns (qualified_posts, any_subreddit_reachable)."""
    posts: list[QualifiedPost] = []
    any_reachable = False

    for subreddit in config.subreddits:
        url = f"https://www.reddit.com/r/{subreddit}/hot.json"
        try:
            resp = _get_with_retry(session, url, params={"limit": 50}, sleep=sleep)
            payload = resp.json()
        except Exception as exc:
            record_issue("scraper.reddit", f"Error - Unreachable r/{subreddit}: {exc}")
            continue

        any_reachable = True
        for child in payload.get("data", {}).get("children", []):
            post = child.get("data", {})
            if post.get("stickied"):
                continue

            upvotes = post.get("ups")
            comments = post.get("num_comments")
            if upvotes is None or comments is None:
                record_issue(
                    "scraper.reddit",
                    "missing score/comments field, dropping post",
                    item_id=post.get("id"),
                )
                continue

            if not qualify_reddit_post(upvotes, comments, config.reddit_ratio):
                continue

            posts.append(
                QualifiedPost(
                    id=post.get("id", ""),
                    source="reddit",
                    title=post.get("title", ""),
                    url=post.get("url") or f"https://reddit.com{post.get('permalink', '')}",
                    score=upvotes,
                    comments=comments,
                    subreddit=subreddit,
                    qualified_at=datetime.now(timezone.utc).isoformat(),
                )
            )

    return posts, any_reachable


def run(
    config: Config,
    run_dir: Path,
    *,
    session=requests,
    sleep=time.sleep,
) -> tuple[list[QualifiedPost], bool]:
    """Idempotent: if qualified_posts.json already exists for this run_dir
    (i.e. already run today), returns the cached result instead of
    re-polling. Returns (qualified_posts, any_source_reachable)."""
    out_path = run_dir / "qualified_posts.json"
    meta_path = run_dir / "qualified_posts.meta.json"

    if out_path.exists():
        logger.info("Scraper: already run today, using cached %s", out_path)
        raw = json.loads(out_path.read_text())
        reachable = True
        if meta_path.exists():
            reachable = json.loads(meta_path.read_text()).get("any_source_reachable", True)
        return [QualifiedPost(**item) for item in raw], reachable

    hn_posts, hn_ok = fetch_hackernews(config, session=session, sleep=sleep)
    reddit_posts, reddit_ok = fetch_reddit(config, session=session, sleep=sleep)
    posts = hn_posts + reddit_posts
    any_reachable = hn_ok or reddit_ok

    run_dir.mkdir(parents=True, exist_ok=True)
    dump_json(out_path, posts)
    meta_path.write_text(json.dumps({"any_source_reachable": any_reachable}))

    return posts, any_reachable
