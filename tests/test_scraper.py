"""Pytest mapping of the Scraper Agent's Gherkin acceptance criteria in
CLAUDE.md section 3.2."""
from __future__ import annotations

import requests

from agents import scraper
from agents.config import Config
from tests.conftest import FakeResponse, fake_session


# Scenario: High-signal HN post qualifies / Low-signal HN post is dropped
def test_hn_post_with_exactly_threshold_points_qualifies():
    assert scraper.qualify_hn_post(200, threshold=200) is True


def test_hn_post_below_threshold_is_dropped():
    assert scraper.qualify_hn_post(199, threshold=200) is False


# Scenario: Reddit post meets ratio / fails ratio
def test_reddit_post_meeting_ratio_qualifies():
    assert scraper.qualify_reddit_post(500, 40, ratio=10) is True  # 12.5:1


def test_reddit_post_failing_ratio_is_dropped():
    assert scraper.qualify_reddit_post(500, 100, ratio=10) is False  # 5:1


# Scenario: Config-driven threshold change
def test_threshold_is_config_driven_not_hardcoded():
    assert scraper.qualify_hn_post(299, threshold=300) is False
    assert scraper.qualify_hn_post(300, threshold=300) is True


# Scenario: Rate limited
def test_get_with_retry_pauses_and_retries_on_429_then_succeeds():
    calls = {"n": 0}

    def get(url, params=None, headers=None, timeout=None):
        calls["n"] += 1
        if calls["n"] < 3:
            return FakeResponse(status_code=429)
        return FakeResponse(status_code=200, json_data={"ok": True})

    sleeps = []
    resp = scraper._get_with_retry(fake_session(get), "http://x", sleep=sleeps.append)

    assert resp.json() == {"ok": True}
    assert sleeps == [60, 60]


def test_get_with_retry_gives_up_after_max_attempts():
    def get(url, params=None, headers=None, timeout=None):
        return FakeResponse(status_code=429)

    sleeps = []
    try:
        scraper._get_with_retry(fake_session(get), "http://x", sleep=sleeps.append)
        assert False, "expected HTTPError"
    except requests.HTTPError:
        pass

    assert sleeps == [60, 60, 60]


# Scenario: Source unreachable
def test_fetch_hackernews_marks_unreachable_when_api_down():
    def get(url, params=None, headers=None, timeout=None):
        raise requests.ConnectionError("down")

    posts, reachable = scraper.fetch_hackernews(Config(), session=fake_session(get), sleep=lambda s: None)

    assert posts == []
    assert reachable is False


def test_fetch_reddit_continues_with_reachable_subreddit_when_one_is_down():
    def get(url, params=None, headers=None, timeout=None):
        if "artificial" in url:
            raise requests.ConnectionError("down")
        return FakeResponse(
            200,
            json_data={
                "data": {
                    "children": [
                        {
                            "data": {
                                "id": "abc",
                                "title": "t",
                                "url": "http://x",
                                "ups": 500,
                                "num_comments": 40,
                                "stickied": False,
                            }
                        }
                    ]
                }
            },
        )

    config = Config(subreddits=["artificial", "MachineLearning"], reddit_ratio=10)
    posts, reachable = scraper.fetch_reddit(config, session=fake_session(get), sleep=lambda s: None)

    assert reachable is True
    assert len(posts) == 1
    assert posts[0].subreddit == "MachineLearning"


def test_run_continues_with_only_reddit_when_hn_is_down(monkeypatch, tmp_path):
    monkeypatch.setattr(scraper, "fetch_hackernews", lambda config, **kw: ([], False))
    monkeypatch.setattr(
        scraper,
        "fetch_reddit",
        lambda config, **kw: (
            [scraper.QualifiedPost(id="1", source="reddit", title="t", url="http://x", score=500,
                                    comments=40, subreddit="artificial", qualified_at="now")],
            True,
        ),
    )
    posts, any_reachable = scraper.run(Config(), tmp_path / "2026-01-01")

    assert any_reachable is True
    assert len(posts) == 1


# Malformed/missing score field -> drop, log, don't crash
def test_fetch_hackernews_drops_post_with_missing_score():
    def get(url, params=None, headers=None, timeout=None):
        if "topstories" in url:
            return FakeResponse(200, json_data=[1])
        return FakeResponse(200, json_data={"id": 1, "type": "story", "title": "no score"})

    posts, reachable = scraper.fetch_hackernews(Config(), session=fake_session(get), sleep=lambda s: None)

    assert posts == []
    assert reachable is True


# Idempotency: rerunning the same day should not re-poll
def test_run_is_idempotent_for_the_same_run_dir(tmp_path):
    calls = {"n": 0}

    def get(url, params=None, headers=None, timeout=None):
        calls["n"] += 1
        if "topstories" in url:
            return FakeResponse(200, json_data=[])
        return FakeResponse(200, json_data={"data": {"children": []}})

    config = Config(subreddits=[])
    run_dir = tmp_path / "2026-01-01"

    posts1, ok1 = scraper.run(config, run_dir, session=fake_session(get), sleep=lambda s: None)
    calls_after_first_run = calls["n"]
    posts2, ok2 = scraper.run(config, run_dir, session=fake_session(get), sleep=lambda s: None)

    assert calls["n"] == calls_after_first_run  # no new HTTP calls on the second run
    assert posts1 == posts2
    assert ok1 == ok2
