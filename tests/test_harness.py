from datetime import datetime, timedelta, timezone

from newser import harness
from newser.fetchers.base import Fetcher
from newser.models import NewsItem


class FakeFetcher(Fetcher):
    def __init__(self, source_key: str, items: list[NewsItem]) -> None:
        self.source_key = source_key
        self._items = items

    def fetch(self) -> list[NewsItem]:
        return self._items


class BrokenFetcher(Fetcher):
    source_key = "broken"

    def fetch(self) -> list[NewsItem]:
        raise RuntimeError("simulated network failure")


def make_item(title: str, source_key: str, **kwargs) -> NewsItem:
    return NewsItem(
        title=title,
        url=f"https://example.com/{title}",
        source_key=source_key,
        source_name=source_key,
        published=datetime.now(timezone.utc) - timedelta(hours=1),
        **kwargs,
    )


def test_build_digest_groups_items_into_sections(monkeypatch):
    fetchers = [
        FakeFetcher("hackernews", [make_item("Story A", "hackernews", score=100)]),
        FakeFetcher("arxiv", [make_item("Paper B", "arxiv")]),
    ]
    monkeypatch.setattr(harness, "build_fetchers", lambda enabled_sources=None: fetchers)

    digest = harness.build_digest()

    assert digest.total_items == 2
    assert digest.source_count == 2
    section_keys = {s.key for s in digest.sections}
    assert section_keys == {"hackernews", "arxiv"}


def test_build_digest_deduplicates_across_sources(monkeypatch):
    fetchers = [
        FakeFetcher("techcrunch_ai", [make_item("Same Story Twice", "techcrunch_ai")]),
        FakeFetcher("google_news_ai", [make_item("same story twice", "google_news_ai")]),
    ]
    monkeypatch.setattr(harness, "build_fetchers", lambda enabled_sources=None: fetchers)

    digest = harness.build_digest()

    assert digest.total_items == 1
    assert digest.sections[0].key == "techcrunch_ai"


def test_build_digest_survives_a_broken_fetcher(monkeypatch):
    fetchers = [
        FakeFetcher("hackernews", [make_item("Still Works", "hackernews")]),
        BrokenFetcher(),
    ]
    monkeypatch.setattr(harness, "build_fetchers", lambda enabled_sources=None: fetchers)

    digest = harness.build_digest()

    assert digest.total_items == 1
    assert digest.sections[0].key == "hackernews"


def test_build_digest_respects_max_per_source(monkeypatch):
    items = [make_item(f"Story {i}", "hackernews") for i in range(5)]
    fetchers = [FakeFetcher("hackernews", items)]
    monkeypatch.setattr(harness, "build_fetchers", lambda enabled_sources=None: fetchers)

    digest = harness.build_digest(max_per_source=2)

    assert digest.total_items == 2
