# Glueball — Issue Log & Continuous Improvement Ledger

This file tracks every distinct class of problem the harness has hit, either
during development or during a live daily run, per the Continuous
Improvement Protocol in `CLAUDE.md` (section 9).

`agents/issue_log.py` appends automatically to "Open observations" the first
time a new runtime issue signature (`component` + `message`) is seen, using
every call's entry in `runs/run_log.json` as the source of truth. Issues
found during development or code review that never went through a live
pipeline run should be added to "Open observations" by hand instead.

A human or Claude Code moves an entry from "Open observations" to
"Resolved" only once a real code fix has shipped and a regression test
guards it — not when the symptom merely stops appearing.

## Resolved

- **Test suite polluted real `ISSUES.md` / `runs/run_log.json`.** The first
  full `pytest` run against this codebase revealed that `agents/issue_log.py`
  writes to its module-level `RUN_LOG_PATH` / `ISSUES_MD_PATH` constants
  unconditionally, and most agent tests exercise real error-handling paths
  (that's the point of the acceptance-criteria tests) -- so every test run
  was appending real entries to the actual repo files as a side effect.
  Fixed by adding an `autouse` fixture (`tests/conftest.py:_isolate_issue_log`)
  that redirects both paths into the test's own `tmp_path` for every test in
  the suite. Guarded by `tests/test_issue_log.py`, which explicitly asserts
  on `record_issue()`'s file-writing behavior against isolated paths.

## Open observations

<!-- OPEN-OBSERVATIONS -->
- [0a4b8d3dd51a] `scraper.hackernews`: missing score field, dropping post (first seen 2026-08-07)

- [c8b6093bd712] `scraper.reddit`: Error - Unreachable r/artificial: down (first seen 2026-08-07)

- [2ab24ab1c220] `scraper.hackernews`: Error - Unreachable: down (first seen 2026-08-07)

- [1fc300959818] `orchestrator`: All sources unreachable after whole-run retry; previous digest left unchanged (first seen 2026-08-07)

- [4a86a475bc47] `extractor`: bot-block page detected: http://blocked.example.com (first seen 2026-08-07)

- [a61ab436e112] `extractor`: failed to fetch http://example.com/article: dns failure (first seen 2026-08-07)

- [6e492dda25ca] `extractor`: HTTP 404 for http://example.com/article (first seen 2026-08-07)

- [8df432dac3ac] `extractor`: bot-blocked (403): http://example.com/article (first seen 2026-08-07)

- [78bae1a6a711] `extractor`: bot-block page detected: http://example.com/article (first seen 2026-08-07)

- [4b886f0ff125] `editor`: LLM call failed for 1: API down (first seen 2026-08-07)

- [a37b0d15e723] `editor`: brief still missing a required section for 1, dropping (first seen 2026-08-07)

- [6e9d64c86e30] `editor`: brief malformed or out of word range (4) for 1, retrying (first seen 2026-08-07)

- [9e65a26c8ebf] `editor`: brief still out of word range (450) after retry for 1; truncating and publishing with flag (first seen 2026-08-07)

- [c363b3739f87] `editor`: brief malformed or out of word range (450) for 1, retrying (first seen 2026-08-07)

- [9d6576b892b5] `classifier`: LLM call failed for 1: API down (first seen 2026-08-07)

- [7f4cd24087fa] `classifier`: no confident tag for 1, using fallback (first seen 2026-08-07)

