"""Extractor Agent -- fetches full body text for qualified URLs, strips
boilerplate (script/style/nav tags), and marks bot-blocked or unreachable
pages instead of crashing the pipeline."""
from __future__ import annotations

import logging
import re
from pathlib import Path

import requests

from agents.issue_log import record_issue
from agents.models import QualifiedPost, RawArticle, dump_json, load_json

logger = logging.getLogger(__name__)

USER_AGENT = "glueball-agent/0.1 (+https://github.com/satyansh-Srivastava/newser)"
REQUEST_TIMEOUT = 15

_SCRIPT_STYLE_RE = re.compile(r"<(script|style)[^>]*>.*?</\1>", re.DOTALL | re.IGNORECASE)
_ANY_TAG_RE = re.compile(r"<[^>]+>")

BOT_BLOCK_MARKERS = (
    "captcha",
    "access denied",
    "are you a robot",
    "cf-browser-verification",
    "verify you are human",
)


def _clean_html(html: str) -> str:
    text = _SCRIPT_STYLE_RE.sub(" ", html)
    text = _ANY_TAG_RE.sub(" ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def _failed(post: QualifiedPost) -> RawArticle:
    return RawArticle(
        id=post.id, url=post.url, title=post.title, source=post.source,
        body_text="", extraction_status="failed",
    )


def _blocked(post: QualifiedPost) -> RawArticle:
    return RawArticle(
        id=post.id, url=post.url, title=post.title, source=post.source,
        body_text="", extraction_status="blocked",
    )


def extract_one(post: QualifiedPost, *, session=requests) -> RawArticle:
    try:
        resp = session.get(post.url, headers={"User-Agent": USER_AGENT}, timeout=REQUEST_TIMEOUT)
    except Exception as exc:
        record_issue("extractor", f"failed to fetch {post.url}: {exc}", item_id=post.id)
        return _failed(post)

    if resp.status_code == 403:
        record_issue("extractor", f"bot-blocked (403): {post.url}", item_id=post.id)
        return _blocked(post)

    if resp.status_code == 404 or resp.status_code >= 500:
        record_issue("extractor", f"HTTP {resp.status_code} for {post.url}", item_id=post.id)
        return _failed(post)

    if resp.status_code >= 400:
        record_issue("extractor", f"HTTP {resp.status_code} for {post.url}", item_id=post.id)
        return _failed(post)

    body = _clean_html(resp.text or "")
    if any(marker in body.lower() for marker in BOT_BLOCK_MARKERS):
        record_issue("extractor", f"bot-block page detected: {post.url}", item_id=post.id)
        return _blocked(post)

    if not body:
        record_issue("extractor", f"empty body extracted: {post.url}", item_id=post.id)
        return _failed(post)

    return RawArticle(
        id=post.id, url=post.url, title=post.title, source=post.source,
        body_text=body, extraction_status="success",
    )


def run(qualified_posts: list[QualifiedPost], run_dir: Path, *, session=requests) -> list[RawArticle]:
    out_path = run_dir / "raw_articles.json"
    if out_path.exists():
        raw = load_json(out_path)
        return [RawArticle(**item) for item in raw]

    articles = [extract_one(post, session=session) for post in qualified_posts]

    run_dir.mkdir(parents=True, exist_ok=True)
    dump_json(out_path, articles)
    return articles
