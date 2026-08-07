"""Structured issue/error logging shared by every agent.

This is the runtime half of the Continuous Improvement Protocol in
CLAUDE.md (section 9): every call to record_issue() appends a structured
entry to runs/run_log.json, and -- the first time a given (component,
message) signature is seen -- also appends a bullet to ISSUES.md under
"Open observations", so it surfaces for a real code fix + regression test
rather than just accumulating silently in a log file nobody reads.
"""
from __future__ import annotations

import hashlib
import json
import logging
from datetime import datetime, timezone
from pathlib import Path

logger = logging.getLogger(__name__)

REPO_ROOT = Path(__file__).resolve().parent.parent
RUN_LOG_PATH = REPO_ROOT / "runs" / "run_log.json"
ISSUES_MD_PATH = REPO_ROOT / "ISSUES.md"
OPEN_OBSERVATIONS_MARKER = "<!-- OPEN-OBSERVATIONS -->"


def _signature(component: str, message: str) -> str:
    return hashlib.sha1(f"{component}:{message}".encode()).hexdigest()[:12]


def _load_entries() -> list[dict]:
    if not RUN_LOG_PATH.exists():
        return []
    try:
        return json.loads(RUN_LOG_PATH.read_text())
    except json.JSONDecodeError:
        return []


def record_issue(
    component: str,
    message: str,
    *,
    item_id: str | None = None,
    severity: str = "warning",
) -> None:
    """Log an issue encountered by any agent. Never raises -- a broken
    logger must not be allowed to take down the pipeline it's logging for."""
    logger.warning("[%s] %s", component, message)
    try:
        RUN_LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
        entries = _load_entries()
        sig = _signature(component, message)
        seen_before = any(e.get("signature") == sig for e in entries)

        entries.append(
            {
                "ts": datetime.now(timezone.utc).isoformat(),
                "component": component,
                "message": message,
                "item_id": item_id,
                "severity": severity,
                "signature": sig,
            }
        )
        RUN_LOG_PATH.write_text(json.dumps(entries, indent=2))

        if not seen_before:
            _append_open_observation(component, message, sig)
    except OSError as exc:  # disk full, read-only fs, etc.
        logger.error("issue_log: failed to persist issue log entry: %s", exc)


def _append_open_observation(component: str, message: str, sig: str) -> None:
    if not ISSUES_MD_PATH.exists():
        return
    text = ISSUES_MD_PATH.read_text()
    if sig in text:
        return
    bullet = f"- [{sig}] `{component}`: {message} (first seen {datetime.now(timezone.utc).date()})\n"
    if OPEN_OBSERVATIONS_MARKER in text:
        text = text.replace(OPEN_OBSERVATIONS_MARKER, OPEN_OBSERVATIONS_MARKER + "\n" + bullet, 1)
    else:
        text = text.rstrip("\n") + "\n" + bullet
    ISSUES_MD_PATH.write_text(text)
