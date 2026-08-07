# Glueball

An autonomous, no-human-in-loop multi-agent pipeline that scrapes AI
discussion from Hacker News and Reddit, filters it to high-signal posts,
synthesizes each into a 2-minute What/Why/Who business brief via the
Claude API, tags it against a locked taxonomy, and publishes a single
static, light-mode-only HTML digest to GitHub Pages.

The full build spec lives in [`CLAUDE.md`](./CLAUDE.md) — that file is fed
to Claude Code as project context automatically. Section 9 of it
(**Continuous Improvement Protocol**) is a standing instruction: every real
issue this harness hits gets logged, fixed in code, covered by a
regression test, and recorded in [`ISSUES.md`](./ISSUES.md) — not just
patched and forgotten.

## Architecture

```
Orchestrator (agents/orchestrator.py)
   │
   ├─▶ Scraper    (agents/scraper.py)     → runs/<date>/qualified_posts.json
   ├─▶ Extractor  (agents/extractor.py)   → runs/<date>/raw_articles.json
   ├─▶ Editor     (agents/editor.py)      → runs/<date>/briefs.json
   ├─▶ Classifier (agents/classifier.py)  → runs/<date>/tagged_briefs.json
   └─▶ Publisher  (agents/publisher.py)   → docs/index.html (+ docs/archive/)
```

Each agent is a discrete unit with a defined JSON input/output contract
(see `agents/models.py` and CLAUDE.md section 3), so any stage can be
rerun, retried, or replaced independently. Every agent's own retry/failure
rules (429 backoff, bot-block detection, malformed-field handling,
word-count retry, taxonomy fallback) are implemented exactly per the
Gherkin acceptance criteria in CLAUDE.md, and each has a matching pytest
file under `tests/`.

**Only Hacker News + Reddit are sources** (per spec) — qualification is
threshold-based, not keyword-based: an HN post qualifies at
`score >= hn_threshold`; a Reddit post qualifies at
`upvotes / max(comments, 1) >= reddit_ratio`. All thresholds, the
subreddit list, the taxonomy, and the brief word range live in
[`config.yaml`](./config.yaml) — nothing is hardcoded, and editing that
file + committing is the only way to change runtime behavior (no admin UI,
no login panel, per CLAUDE.md section 2).

## Running locally

```bash
pip install -r requirements.txt
```

**API key:** copy `.env.example` to `.env` in the repo root and fill in your
real key:

```bash
cp .env.example .env
# then edit .env so it reads:  ANTHROPIC_API_KEY=sk-ant-...
```

`.env` is gitignored, so it never gets committed. `main.py` loads it
automatically on every run (via `python-dotenv`) -- no `export` needed. If
you'd rather set it as a real environment variable instead, that still
works too and takes the same effect.

```bash
python main.py                        # writes docs/index.html + docs/archive/
python main.py --output-dir docs -v   # verbose logging
python main.py --config config.yaml
```

Each day's intermediate artifacts and a run summary land under
`runs/<YYYY-MM-DD>/` and `runs/<YYYY-MM-DD>.json`; rerunning the same day
is a no-op (the orchestrator and each agent check for existing output
before doing any work again).

## Automation (GitHub Actions + GitHub Pages)

`.github/workflows/daily-digest.yml` runs the pipeline daily at 23:00 UTC
(matching `config.yaml`'s `schedule_cron`) and on manual dispatch, then
commits the regenerated `docs/`, `runs/`, and `ISSUES.md` back to the repo.

One-time setup:
1. Add an **`ANTHROPIC_API_KEY`** repository secret (Settings → Secrets and
   variables → Actions) — required for the Editor and Classifier agents.
2. Go to **Settings → Pages**, set **Source: Deploy from a branch**,
   **Branch: `main` / `docs`**, and save.
3. Your digest will be live at `https://<user>.github.io/<repo>/` after
   the next workflow run (or trigger one manually from the **Actions** tab).

## Tests

```bash
pip install -r requirements-dev.txt
pytest
```

Every Gherkin scenario in `CLAUDE.md` section 3 has a corresponding pytest
case (see `tests/test_scraper.py`, `test_extractor.py`, `test_editor.py`,
`test_classifier.py`, `test_publisher.py`, `test_orchestrator.py`). No test
makes a real network or LLM call — HTTP is faked via a minimal
session-like object (`tests/conftest.py:fake_session`) and the LLM via
`tests/conftest.py:FakeLLM`. An autouse fixture also redirects
`agents/issue_log.py`'s output into a temp directory for every test, so
running the suite never mutates the real `ISSUES.md` / `runs/run_log.json`
(see the first entry in `ISSUES.md`'s Resolved section for why that
fixture exists).

## Continuous improvement

`agents/issue_log.py:record_issue()` is called by every agent on every
handled failure. It always appends a structured entry to
`runs/run_log.json`, and — the first time a given `(component, message)`
signature is seen — also appends a bullet to `ISSUES.md` under "Open
observations". That's the prompt for a human or Claude Code to ship a real
fix (with a regression test) and move the entry to "Resolved". See
CLAUDE.md section 9 for the full protocol.
