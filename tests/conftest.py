"""Shared test fixtures/helpers -- a fake requests.Session so no test in
this suite ever makes a real network or LLM call."""
from __future__ import annotations

from types import SimpleNamespace

import pytest
import requests

from agents import issue_log


@pytest.fixture(autouse=True)
def _isolate_issue_log(tmp_path, monkeypatch):
    """Every agent funnels warnings/errors through agents.issue_log, which
    by default writes to the real repo's runs/run_log.json and ISSUES.md.
    Without this, any test that exercises real error-handling paths (most
    of them do, by design -- that's what the acceptance criteria are)
    pollutes the actual project files as a side effect of running the
    suite. Redirect both paths into the test's own tmp_path so the test
    suite never mutates real repo state. (See ISSUES.md: this was caught
    by the very first full test run and fixed here.)"""
    monkeypatch.setattr(issue_log, "RUN_LOG_PATH", tmp_path / "runs" / "run_log.json")
    monkeypatch.setattr(issue_log, "ISSUES_MD_PATH", tmp_path / "ISSUES.md")


class FakeResponse:
    def __init__(self, status_code=200, json_data=None, text=""):
        self.status_code = status_code
        self._json = json_data
        self.text = text

    def json(self):
        return self._json

    def raise_for_status(self):
        if self.status_code >= 400:
            raise requests.HTTPError(f"{self.status_code} error")


def fake_session(get_fn):
    """Wraps a plain function as a requests.Session-like object exposing
    only the .get method our agents actually call."""
    return SimpleNamespace(get=get_fn)


class FakeLLM:
    """Returns each queued response in order; raises if exhausted."""

    def __init__(self, responses):
        self.responses = list(responses)
        self.calls: list[tuple[str, str]] = []

    def complete(self, system: str, user: str) -> str:
        self.calls.append((system, user))
        if not self.responses:
            raise RuntimeError("FakeLLM: no more queued responses")
        return self.responses.pop(0)
