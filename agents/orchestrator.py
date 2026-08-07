"""Orchestrator -- runs Scraper -> Extractor -> Editor -> Classifier ->
Publisher in strict sequence, owns the whole-run retry/failure-escalation
rule, and writes the daily run summary. See CLAUDE.md section 9: any new
failure class hit here should get a real code fix + regression test, not
just a log line -- that's what ISSUES.md is for.
"""
from __future__ import annotations

import json
import logging
import time
from datetime import datetime, timezone
from pathlib import Path

from agents import classifier, editor, extractor, publisher, scraper
from agents.config import Config
from agents.issue_log import RUN_LOG_PATH, record_issue

logger = logging.getLogger(__name__)

REPO_ROOT = Path(__file__).resolve().parent.parent
RUNS_DIR = REPO_ROOT / "runs"

WHOLE_RUN_RETRY_DELAY_SECONDS = 600  # 10 minutes, per CLAUDE.md 3.1


def _error_count() -> int:
    if not RUN_LOG_PATH.exists():
        return 0
    try:
        return len(json.loads(RUN_LOG_PATH.read_text()))
    except json.JSONDecodeError:
        return 0


def run(config: Config | None = None, *, output_dir: str = "docs", sleep=time.sleep) -> dict:
    config = config or Config.load()
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    run_dir = RUNS_DIR / today
    summary_path = RUNS_DIR / f"{today}.json"

    if summary_path.exists():
        logger.info("Orchestrator: already completed today's run (%s); skipping.", summary_path)
        return json.loads(summary_path.read_text())

    errors_before = _error_count()

    qualified, any_source_reachable = scraper.run(config, run_dir, sleep=sleep)

    if not any_source_reachable:
        logger.warning(
            "Both sources unreachable; retrying whole run once in %ss per CLAUDE.md 3.1",
            WHOLE_RUN_RETRY_DELAY_SECONDS,
        )
        sleep(WHOLE_RUN_RETRY_DELAY_SECONDS)
        for cached in (run_dir / "qualified_posts.json", run_dir / "qualified_posts.meta.json"):
            if cached.exists():
                cached.unlink()
        qualified, any_source_reachable = scraper.run(config, run_dir, sleep=sleep)

    if not any_source_reachable:
        record_issue(
            "orchestrator",
            "All sources unreachable after whole-run retry; previous digest left unchanged",
        )
        summary = {
            "date": today,
            "scraped": 0,
            "extracted": 0,
            "briefed": 0,
            "published": "unchanged (previous digest retained)",
            "any_source_reachable": False,
            "errors": _error_count() - errors_before,
        }
        RUNS_DIR.mkdir(parents=True, exist_ok=True)
        summary_path.write_text(json.dumps(summary, indent=2))
        return summary

    raw_articles = extractor.run(qualified, run_dir)
    briefs = editor.run(raw_articles, config, run_dir)
    tagged = classifier.run(briefs, config, run_dir)
    publisher.run(tagged, config, output_dir=output_dir)

    summary = {
        "date": today,
        "scraped": len(qualified),
        "extracted": len(raw_articles),
        "briefed": len(briefs),
        "published": len(tagged),
        "any_source_reachable": True,
        "errors": _error_count() - errors_before,
    }
    RUNS_DIR.mkdir(parents=True, exist_ok=True)
    summary_path.write_text(json.dumps(summary, indent=2))
    return summary
