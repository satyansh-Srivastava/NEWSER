"""Pytest coverage of the Orchestrator's sequencing/retry/idempotency rules
in CLAUDE.md section 3.1."""
from __future__ import annotations

import json
from datetime import datetime, timezone

from agents import classifier, editor, extractor, orchestrator, publisher, scraper
from agents.config import Config
from agents.models import Brief, QualifiedPost, RawArticle, TaggedBrief


def test_orchestrator_runs_full_pipeline_in_sequence(tmp_path, monkeypatch):
    monkeypatch.setattr(orchestrator, "RUNS_DIR", tmp_path / "runs")

    fake_post = QualifiedPost(id="1", source="hackernews", title="t", url="http://x",
                               score=250, comments=5, subreddit=None, qualified_at="now")
    monkeypatch.setattr(scraper, "run", lambda config, run_dir, sleep=None: ([fake_post], True))
    monkeypatch.setattr(
        extractor, "run",
        lambda posts, run_dir: [RawArticle(id="1", url="http://x", title="t", source="hackernews",
                                            body_text="b", extraction_status="success")],
    )
    monkeypatch.setattr(
        editor, "run",
        lambda articles, config, run_dir: [Brief(id="1", title="t", what="w", why="w", who="w",
                                                   source_url="http://x", word_count=200)],
    )
    monkeypatch.setattr(
        classifier, "run",
        lambda briefs, config, run_dir: [TaggedBrief(id="1", title="t", what="w", why="w", who="w",
                                                       source_url="http://x", word_count=200, tags=["Funding"])],
    )
    published = {}
    monkeypatch.setattr(
        publisher, "run",
        lambda tagged, config, output_dir="docs": published.setdefault("tagged", tagged),
    )

    summary = orchestrator.run(Config(), output_dir=str(tmp_path / "docs"), sleep=lambda s: None)

    assert summary["scraped"] == 1
    assert summary["extracted"] == 1
    assert summary["briefed"] == 1
    assert summary["published"] == 1
    assert published["tagged"][0].id == "1"


def test_orchestrator_retries_once_then_gives_up_on_total_outage(tmp_path, monkeypatch):
    monkeypatch.setattr(orchestrator, "RUNS_DIR", tmp_path / "runs")
    monkeypatch.setattr(scraper, "run", lambda config, run_dir, sleep=None: ([], False))

    sleeps = []
    summary = orchestrator.run(Config(), output_dir=str(tmp_path / "docs"), sleep=sleeps.append)

    assert sleeps == [600]  # 10 minutes, once
    assert summary["published"] == "unchanged (previous digest retained)"
    assert summary["any_source_reachable"] is False


def test_orchestrator_recovers_if_retry_succeeds(tmp_path, monkeypatch):
    monkeypatch.setattr(orchestrator, "RUNS_DIR", tmp_path / "runs")

    fake_post = QualifiedPost(id="1", source="hackernews", title="t", url="http://x",
                               score=250, comments=5, subreddit=None, qualified_at="now")
    call_count = {"n": 0}

    def fake_scraper_run(config, run_dir, sleep=None):
        call_count["n"] += 1
        if call_count["n"] == 1:
            return [], False
        return [fake_post], True

    monkeypatch.setattr(scraper, "run", fake_scraper_run)
    monkeypatch.setattr(extractor, "run", lambda posts, run_dir: [])
    monkeypatch.setattr(editor, "run", lambda articles, config, run_dir: [])
    monkeypatch.setattr(classifier, "run", lambda briefs, config, run_dir: [])
    monkeypatch.setattr(publisher, "run", lambda tagged, config, output_dir="docs": None)

    sleeps = []
    summary = orchestrator.run(Config(), output_dir=str(tmp_path / "docs"), sleep=sleeps.append)

    assert sleeps == [600]
    assert summary["scraped"] == 1
    assert summary["any_source_reachable"] is True


def test_orchestrator_skips_a_second_run_the_same_day(tmp_path, monkeypatch):
    monkeypatch.setattr(orchestrator, "RUNS_DIR", tmp_path / "runs")
    (tmp_path / "runs").mkdir()
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    (tmp_path / "runs" / f"{today}.json").write_text(json.dumps({"date": today, "scraped": 5}))

    called = {"n": 0}
    monkeypatch.setattr(scraper, "run", lambda *a, **kw: called.__setitem__("n", called["n"] + 1) or ([], True))

    summary = orchestrator.run(Config(), output_dir=str(tmp_path / "docs"))

    assert called["n"] == 0
    assert summary["scraped"] == 5
