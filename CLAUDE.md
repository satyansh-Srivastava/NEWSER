# Glueball — Agentic AI Newsletter
## Build Spec for Claude Code

Feed this whole file to Claude Code as the initial prompt / CLAUDE.md. It specifies a fully autonomous, no-human-in-loop, multi-agent pipeline that scrapes AI news, synthesizes it, and publishes a static HTML digest to GitHub Pages.

---

## 1. Product Overview

**Name:** Glueball
**Type:** Autonomous multi-agent workflow, zero human intervention at runtime.
**Output:** A single static HTML page (light mode, minimal, dense) published daily to GitHub Pages, showing curated AI news grouped by tag.

**Value prop:** Ingest noisy AI discussion (HackerNews, Reddit) → filter to high-signal only → synthesize into 2-minute business briefs → publish.

---

## 2. Hard constraints (non-negotiable)

- **No human in the loop at runtime.** No login panels, no manual approval steps, no "Newsletter Admin" UI. All config (thresholds, taxonomy, prompts) lives in a version-controlled config file (`config.yaml`) in the repo. Changing behavior = editing that file and committing — not a runtime actor.
- **Hosting:** GitHub Pages. Output is a static `index.html` (+ assets) written to a `docs/` folder or `gh-pages` branch, deployed via GitHub Actions on a daily cron trigger.
- **Theme:** Light mode only. No dark mode toggle, no theme switcher.
- **Styling:** Minimal, descriptive, dense. Typography-first. Minimize whitespace waste — no giant hero banners, no oversized padding. Card-based or list-based layout grouped by tag category.
- **No email/SMTP delivery in v1.** Distribution = publishing to Pages URL only. (Original SMTP/SendGrid idea dropped — GitHub Pages is the sole delivery mechanism.)

---

## 3. Agent architecture

Five agents, one orchestrator. Each agent is a discrete unit with a defined input/output contract (JSON), so any agent can be rerun, retried, or replaced independently.

```
Orchestrator Agent
   │
   ├─▶ Scraper Agent (HN + Reddit)
   │        │  outputs: qualified_posts.json
   │        ▼
   ├─▶ Extractor Agent (fetch + clean body text)
   │        │  outputs: raw_articles.json
   │        ▼
   ├─▶ Editor Agent (What/Why/Who synthesis)
   │        │  outputs: briefs.json
   │        ▼
   ├─▶ Classifier Agent (taxonomy tagging)
   │        │  outputs: tagged_briefs.json
   │        ▼
   └─▶ Publisher Agent (HTML generation + Pages deploy)
            outputs: docs/index.html
```

### 3.1 Orchestrator Agent
**Owns:** sequencing, retries, failure escalation, run logging.
**Trigger:** GitHub Actions cron, once daily (EOD, e.g. 23:00 UTC).
**Behavior:**
- Runs agents in strict sequence above.
- If an agent fails after 2 retries, log the failure to `run_log.json`, skip that agent's non-critical output (e.g. one bad article), and continue pipeline — never halt the whole run for a single item failure.
- If Scraper Agent itself fails entirely (API down), retry whole run once after 10 min; if still failing, publish previous day's page unchanged and log incident.
- Writes a run summary (`runs/YYYY-MM-DD.json`) with: items scraped, items qualified, items dropped, items published, errors.

### 3.2 Scraper Agent
**Owns:** polling HN + Reddit, applying qualification thresholds, output = list of qualified URLs only (no body text yet — do not spend tokens/bandwidth on unqualified posts).

**Input:** none (polls live APIs)
**Output schema (`qualified_posts.json`):**
```json
[
  {
    "id": "string",
    "source": "hackernews | reddit",
    "title": "string",
    "url": "string",
    "score": "number",
    "comments": "number",
    "subreddit": "string | null",
    "qualified_at": "ISO8601"
  }
]
```

**Rules:**
- HackerNews: EOD poll, top posts. Qualify if `points >= config.hn_threshold` (default 200).
- Reddit: poll `config.subreddits` (default: r/artificial, r/MachineLearning, r/SaaS). Qualify if `upvotes / max(comments,1) >= config.reddit_ratio` (default 10:1).
- Run once per day only — orchestrator enforces this, agent itself should be idempotent (safe to no-op if already run today).
- On HTTP 429: pause 60s, retry, max 3 attempts, then mark source unreachable for this run and continue with other source.
- On source totally unreachable: log `"Error - Unreachable"`, continue pipeline with whatever source succeeded.
- Malformed/missing score field → treat post as failed threshold, drop, log warning (do not crash).

**Acceptance criteria (Gherkin):**
```gherkin
Scenario: High-signal HN post qualifies
  Given the HN EOD poll runs
  When a post has exactly 200 points
  Then it is added to qualified_posts.json with source "hackernews"

Scenario: Low-signal HN post is dropped
  Given the HN EOD poll runs
  When a post has 199 points
  Then it is excluded from qualified_posts.json

Scenario: Reddit post meets ratio
  Given a subreddit poll runs
  When a post has 500 upvotes and 40 comments (12.5:1)
  Then it is added to qualified_posts.json with source "reddit"

Scenario: Reddit post fails ratio
  Given a subreddit poll runs
  When a post has 500 upvotes and 100 comments (5:1)
  Then it is excluded from qualified_posts.json

Scenario: Rate limited
  Given the scraper receives HTTP 429
  Then it pauses 60 seconds and retries, up to 3 attempts

Scenario: Source unreachable
  Given HackerNews API is down after retries
  Then the run continues using only Reddit results
  And the failure is logged in run_log.json

Scenario: Config-driven threshold change
  Given config.yaml sets hn_threshold to 300
  When the next EOD run triggers
  Then posts are qualified against 300, not 200
```

### 3.3 Extractor Agent
**Owns:** fetching full body text for qualified URLs only, stripping ads/nav/boilerplate, bypassing basic bot protection.

**Input:** `qualified_posts.json`
**Output schema (`raw_articles.json`):**
```json
[
  {
    "id": "string",
    "url": "string",
    "title": "string",
    "source": "hackernews | reddit",
    "body_text": "string",
    "extraction_status": "success | blocked | failed"
  }
]
```

**Rules:**
- If bot-blocked or 404/paywall: mark `extraction_status: "failed"`, drop item, log — never halt pipeline.
- Strip nav, ads, footers — keep only main article body.

**Acceptance criteria:**
```gherkin
Scenario: Successful extraction
  Given a qualified URL is reachable
  Then body_text is populated and extraction_status is "success"

Scenario: Bot-blocked source
  Given a qualified URL returns a bot-block page
  Then extraction_status is "failed" and item is excluded downstream
  And the pipeline continues with remaining items
```

### 3.4 Editor Agent
**Owns:** LLM summarization into strict What/Why/Who format, ~200-250 words, source attribution.

**Input:** `raw_articles.json`
**Output schema (`briefs.json`):**
```json
[
  {
    "id": "string",
    "title": "string",
    "what": "string",
    "why": "string",
    "who": "string",
    "source_url": "string",
    "word_count": "number"
  }
]
```

**Rules:**
- Reject/retry once if output word count outside 180-280 range.
- Every brief must include all three headers, non-empty.
- Source URL appended at bottom of every brief.

**Acceptance criteria:**
```gherkin
Scenario: Well-formed brief
  Given a cleaned article body
  When the Editor Agent summarizes it
  Then output contains non-empty what/why/who fields
  And word_count is between 180 and 280
  And source_url matches original article URL

Scenario: Oversized output retried
  Given a first summarization exceeds 280 words
  Then the Editor Agent retries once with a tighter prompt
  And if still oversized, publishes with a truncation flag logged
```

### 3.5 Classifier Agent
**Owns:** assigning one or more tags from the locked taxonomy.

**Input:** `briefs.json`
**Output schema (`tagged_briefs.json`):** same as briefs.json + `"tags": ["string"]`

**Locked taxonomy (from config.yaml, editable there only):**
- Use-Case News
- Novel SaaS/Tech
- Open-Source Models
- Policy & Regulation
- Funding

**Rules:**
- Minimum 1 tag, max 3 tags per brief.
- If no tag confidently applies, assign "Use-Case News" as default fallback (never leave untagged).

**Acceptance criteria:**
```gherkin
Scenario: Brief gets tagged
  Given a synthesized brief
  When classified
  Then it has between 1 and 3 tags from the locked taxonomy

Scenario: Ambiguous brief falls back
  Given a brief with no clear taxonomy match
  Then it is tagged "Use-Case News" by default
```

### 3.6 Publisher Agent
**Owns:** compiling tagged briefs into static HTML, grouped by tag, and deploying to GitHub Pages.

**Input:** `tagged_briefs.json`
**Output:** `docs/index.html` (+ minimal CSS, no external heavy assets)

**Design rules:**
- Light mode only, no toggle.
- Minimal, dense, typography-first. No hero images, no large padding blocks.
- Group stories under tag-category headers, in taxonomy order listed above.
- Each brief renders as compact card: title, What/Why/Who, tags, source link.
- Mobile-responsive (single-column collapse).
- Page includes generation date/timestamp.
- Deploy via GitHub Actions: commit `docs/index.html` to `main` (or push to `gh-pages` branch) after generation, triggering Pages rebuild.

**Acceptance criteria:**
```gherkin
Scenario: Page groups by tag
  Given tagged_briefs.json has items across multiple tags
  Then index.html renders sections in taxonomy order
  And each brief appears under all its assigned tags

Scenario: Empty day
  Given zero briefs qualified today
  Then index.html still publishes with a "No qualifying stories today" message
  And previous day's content is not lost (archived, not overwritten silently)

Scenario: Deploy succeeds
  Given index.html is generated
  Then it is committed and pushed
  And GitHub Pages reflects the update within its normal build window
```

---

## 4. Config file (`config.yaml`) — the only "human" touchpoint

```yaml
hn_threshold: 200
reddit_ratio: 10
subreddits:
  - artificial
  - MachineLearning
  - SaaS
taxonomy:
  - Use-Case News
  - Novel SaaS/Tech
  - Open-Source Models
  - Policy & Regulation
  - Funding
schedule_cron: "0 23 * * *"
brief_word_range: [180, 280]
```
Editing this file and committing is the only way to change system behavior. No runtime admin role, no login panel.

---

## 5. Non-functional requirements

- **Latency:** full pipeline (ingestion → Pages deploy) completes within 15 minutes.
- **Resilience:** any single-item failure (bad scrape, bad extraction) is dropped and logged, never halts the run.
- **Idempotency:** rerunning the pipeline same day should not duplicate entries.
- **No secrets in repo:** LLM API key via GitHub Actions secret, never committed.

---

## 6. Success metrics

- Signal-to-noise ratio: qualified posts that survive to publish vs. discarded by Editor for irrelevance.
- Daily publish success rate (page updates without manual intervention).
- CTR on source links (if trackable via simple query params).

---

## 7. Repo structure (suggested)

```
glueball/
├── agents/
│   ├── orchestrator.py
│   ├── scraper.py
│   ├── extractor.py
│   ├── editor.py
│   ├── classifier.py
│   └── publisher.py
├── config.yaml
├── docs/                # GitHub Pages source
│   └── index.html
├── runs/                # daily run logs
├── .github/workflows/
│   └── daily-digest.yml
└── README.md
```

---

## 8. Instruction to Claude Code

Build this exact system in Python. Each agent = one module in `agents/`, each with the input/output JSON contract defined above and its own acceptance criteria implemented as tests (pytest). Build the orchestrator to run them in sequence with the retry/failure rules specified. Build the GitHub Actions workflow to run daily via cron and deploy `docs/index.html` to GitHub Pages. Use `config.yaml` for all tunable values — do not hardcode thresholds. Keep HTML/CSS output light-mode-only, minimal, dense, no external heavy dependencies. No authentication, no admin UI, no email delivery — GitHub Pages is the only output surface.

---

## 9. Continuous Improvement Protocol (harness self-improvement provisions)

This section is a standing instruction, not part of the original spec — added so the harness gets measurably better every time it breaks, instead of just logging and moving on.

**The rule:** every time a real issue is hit — during development, during a live daily run, in review, anywhere — it must go through this loop, not just get patched silently:

1. **Log it.** Runtime failures already flow through `agents/issue_log.py:record_issue()`, which appends a structured entry to `runs/run_log.json` on every call, and — the first time a given `(component, message)` signature is seen — appends a one-line bullet to `ISSUES.md` under "Open observations". Issues found during development/code review that don't go through a running pipeline should be added to that same "Open observations" section by hand.
2. **Fix it in code.** Ship an actual code change that prevents the issue class from recurring (not just a broader `except:` — a real handling rule, same spirit as the existing 429-backoff / bot-block / malformed-field rules in `agents/scraper.py` and `agents/extractor.py`).
3. **Cover it with a regression test.** Add a pytest case in the relevant `tests/test_*.py` that fails without the fix and passes with it — mirroring the Gherkin-scenario-to-pytest mapping already used throughout `tests/`.
4. **Close the loop in `ISSUES.md`.** Move the entry from "Open observations" to "Resolved", noting the fix and the test that now guards it.

No runtime actor may change `config.yaml` thresholds or taxonomy to work around an issue — per section 2's hard constraint, behavior changes still only happen by a human/Claude Code editing `config.yaml` and committing. This protocol governs *code* fixes to error handling, not runtime config mutation.

The intent: `ISSUES.md` should read as a growing record of every failure mode this harness has actually encountered and how it was closed out, so the same class of bug is never debugged twice.
