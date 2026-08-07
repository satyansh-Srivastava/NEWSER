# Newser

An agent harness that fetches AI news every day from several free sources,
groups and deduplicates it, and renders a single visual HTML digest.

**Live digest:** enable GitHub Pages (see below) to get a URL like
`https://<user>.github.io/NEWSER/`.

## Sources

| Source | Method | Notes |
|---|---|---|
| Hacker News | official Firebase API | top stories scanned, filtered by AI keywords |
| r/artificial, r/MachineLearning | Reddit `.json` endpoints | no auth required |
| arXiv cs.AI | RSS | already AI-scoped |
| TechCrunch AI | RSS | category feed |
| VentureBeat AI | RSS | category feed |
| Google News | RSS search for `AI`, last 24h | already AI-scoped |
| Twitter/X lists | -- | **stubbed, disabled** -- needs a paid API tier. See `newser/fetchers/twitter.py`. |

## How it works (the harness)

1. **Fetchers** (`newser/fetchers/`) -- one class per source, each implementing
   `fetch() -> list[NewsItem]`. A fetcher never raises on network/parse
   failure; it logs and returns `[]` so one bad source can't sink the run.
2. **Harness** (`newser/harness.py`) -- runs every fetcher concurrently
   (`ThreadPoolExecutor`), flattens results in a stable priority order, then
   deduplicates by normalized title across sources (so a story that's both on
   TechCrunch and re-surfaced by Google News only appears once), and groups
   what's left into `Section`s.
3. **Filters** (`newser/filters.py`) -- keyword-based AI relevance check
   (used only for Hacker News, since it isn't topically scoped) and the
   cross-source dedupe logic.
4. **Render** (`newser/render.py` + `newser/templates/digest.html.jinja`) --
   renders the digest into a card-based, responsive HTML page (light/dark
   aware), writes it to `docs/index.html`, and archives a dated copy under
   `docs/archive/`.
5. **CLI** (`newser/main.py`) -- wires it all together.

## Running locally

```bash
pip install -r requirements.txt
python -m newser.main                    # writes docs/index.html + docs/archive/
python -m newser.main --dry-run          # fetch + print stats only, no files written
python -m newser.main --sources hackernews,arxiv
python -m newser.main --max-per-source 5
```

Open `docs/index.html` in a browser to view the result.

## Automation (GitHub Actions + GitHub Pages)

`.github/workflows/daily-digest.yml` runs the agent daily (13:00 UTC) and on
manual dispatch, and commits the regenerated `docs/` back to the repo.

One-time setup to publish it:
1. Go to **Settings -> Pages**.
2. Under "Build and deployment", set **Source: Deploy from a branch**.
3. Set **Branch: `main` / `docs`** (root of the `docs` folder).
4. Save. Your digest will be live at `https://<user>.github.io/<repo>/` after
   the next workflow run (or trigger it manually from the **Actions** tab).

## Tests

```bash
pip install -r requirements-dev.txt
pytest
```

Tests cover the keyword filter, cross-source dedupe, harness orchestration
(including a fetcher that raises), and HTML rendering -- all with fixture
data, no network calls.

## Extending

- **New RSS source:** add an entry to `RSS_FEEDS` in `newser/config.py` --
  no new code needed, it reuses `GenericRssFetcher`.
- **New non-RSS source:** subclass `newser.fetchers.base.Fetcher`, add it to
  `newser/harness.py:build_fetchers`, and add a `SECTION_META` entry for
  display name/icon/color.
- **Twitter/X:** implement `newser/fetchers/twitter.py:TwitterFetcher.fetch`
  against the X API (list timelines require a paid tier), then set
  `ENABLE_TWITTER = True` in `newser/config.py`.
- **LLM-written summaries:** this version is template-based (no LLM calls,
  no API key required). To add real narrative summarization, you'd add a
  step in the harness that sends grouped items to an LLM before rendering.
