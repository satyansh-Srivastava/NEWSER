"""Tests for the runtime half of the Continuous Improvement Protocol
(CLAUDE.md section 9): every issue is logged structurally, and a new issue
signature surfaces in ISSUES.md exactly once."""
from __future__ import annotations

import json

from agents import issue_log


def _patch_paths(monkeypatch, tmp_path):
    run_log = tmp_path / "runs" / "run_log.json"
    issues_md = tmp_path / "ISSUES.md"
    issues_md.write_text("# Issues\n\n## Open observations\n\n<!-- OPEN-OBSERVATIONS -->\n")
    monkeypatch.setattr(issue_log, "RUN_LOG_PATH", run_log)
    monkeypatch.setattr(issue_log, "ISSUES_MD_PATH", issues_md)
    return run_log, issues_md


def test_record_issue_appends_structured_entry(monkeypatch, tmp_path):
    run_log, _ = _patch_paths(monkeypatch, tmp_path)

    issue_log.record_issue("scraper.hackernews", "Error - Unreachable: timeout", item_id="42")

    entries = json.loads(run_log.read_text())
    assert len(entries) == 1
    assert entries[0]["component"] == "scraper.hackernews"
    assert entries[0]["item_id"] == "42"


def test_record_issue_adds_new_signature_to_issues_md_once(monkeypatch, tmp_path):
    _, issues_md = _patch_paths(monkeypatch, tmp_path)

    issue_log.record_issue("extractor", "bot-blocked: http://x")
    issue_log.record_issue("extractor", "bot-blocked: http://x")  # same signature again
    issue_log.record_issue("extractor", "bot-blocked: http://y")  # different message, new signature

    text = issues_md.read_text()
    assert text.count("bot-blocked: http://x") == 1
    assert text.count("bot-blocked: http://y") == 1


def test_record_issue_never_raises_on_disk_failure(monkeypatch, tmp_path):
    run_log, _ = _patch_paths(monkeypatch, tmp_path)
    monkeypatch.setattr(issue_log, "RUN_LOG_PATH", tmp_path / "no" / "such" / "dir" / "run_log.json")

    def boom(*a, **kw):
        raise OSError("disk full")

    monkeypatch.setattr(issue_log.Path, "mkdir", boom)

    issue_log.record_issue("scraper", "disk is full apparently")  # must not raise
