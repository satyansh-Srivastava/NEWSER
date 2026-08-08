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
- [ff184bc9360a] `editor`: LLM call failed for 49209385: ANTHROPIC_API_KEY is not set (first seen 2026-08-08)

- [90893254cfca] `editor`: LLM call failed for 49216362: ANTHROPIC_API_KEY is not set (first seen 2026-08-08)

- [227604a8d30b] `editor`: LLM call failed for 49217993: ANTHROPIC_API_KEY is not set (first seen 2026-08-08)

- [d6f247c02a7e] `editor`: LLM call failed for 49207236: ANTHROPIC_API_KEY is not set (first seen 2026-08-08)

- [7b0c4c5a93af] `editor`: LLM call failed for 49135457: ANTHROPIC_API_KEY is not set (first seen 2026-08-08)

- [81c29a7a0c03] `editor`: LLM call failed for 49218179: ANTHROPIC_API_KEY is not set (first seen 2026-08-08)

- [233c8a58748d] `editor`: LLM call failed for 49214468: ANTHROPIC_API_KEY is not set (first seen 2026-08-08)

- [9ae55c2b2c6c] `editor`: LLM call failed for 49214770: ANTHROPIC_API_KEY is not set (first seen 2026-08-08)

- [6d10bcfca130] `editor`: LLM call failed for 49216946: ANTHROPIC_API_KEY is not set (first seen 2026-08-08)

- [bf508199cabc] `editor`: LLM call failed for 49219508: ANTHROPIC_API_KEY is not set (first seen 2026-08-08)

- [b03cb7aee173] `editor`: LLM call failed for 49189457: ANTHROPIC_API_KEY is not set (first seen 2026-08-08)

- [1e333402e15e] `editor`: LLM call failed for 49222189: ANTHROPIC_API_KEY is not set (first seen 2026-08-08)

- [3ca300e64431] `editor`: LLM call failed for 49220609: ANTHROPIC_API_KEY is not set (first seen 2026-08-08)

- [e2bcd4c00f5f] `editor`: LLM call failed for 49221668: ANTHROPIC_API_KEY is not set (first seen 2026-08-08)

- [9602be312b7e] `editor`: LLM call failed for 49220126: ANTHROPIC_API_KEY is not set (first seen 2026-08-08)

- [2029cabf61f7] `editor`: LLM call failed for 49223082: ANTHROPIC_API_KEY is not set (first seen 2026-08-08)

- [2bd6c0333b08] `extractor`: bot-blocked (403): https://www.nytimes.com/2026/08/08/climate/amazon-data-center-texas-pollution.html (first seen 2026-08-08)

- [24e7eca176b9] `extractor`: bot-block page detected: https://blog.cloudflare.com/kitesurf/ (first seen 2026-08-08)

- [83ee55f66c05] `extractor`: bot-blocked (403): https://www.bloomberg.com/news/articles/2026-08-06/us-military-s-cyber-command-unit-grapples-with-cluster-of-deaths-by-suicide (first seen 2026-08-08)

- [5ddd87334d5c] `extractor`: bot-blocked (403): https://mezha.net/eng/bukvy/ca117584_denmark_requires_oral/ (first seen 2026-08-08)

- [a73cf90e2a63] `editor`: LLM call failed for 49150470: ANTHROPIC_API_KEY is not set (first seen 2026-08-07)

- [c1a397f02f73] `editor`: LLM call failed for 49172836: ANTHROPIC_API_KEY is not set (first seen 2026-08-07)

- [a845e7a03469] `editor`: LLM call failed for 49156111: ANTHROPIC_API_KEY is not set (first seen 2026-08-07)

- [3a8f789b1036] `editor`: LLM call failed for 49189075: ANTHROPIC_API_KEY is not set (first seen 2026-08-07)

- [59e64b9b8646] `editor`: LLM call failed for 49170165: ANTHROPIC_API_KEY is not set (first seen 2026-08-07)

- [a6d26a79117f] `editor`: LLM call failed for 49171268: ANTHROPIC_API_KEY is not set (first seen 2026-08-07)

- [5105d2b7a255] `editor`: LLM call failed for 49167448: ANTHROPIC_API_KEY is not set (first seen 2026-08-07)

- [8791188805b9] `editor`: LLM call failed for 49181083: ANTHROPIC_API_KEY is not set (first seen 2026-08-07)

- [8becf677128c] `editor`: LLM call failed for 49146183: ANTHROPIC_API_KEY is not set (first seen 2026-08-07)

- [70eeb1d5dc03] `editor`: LLM call failed for 49193173: ANTHROPIC_API_KEY is not set (first seen 2026-08-07)

- [49c16bfc9d43] `editor`: LLM call failed for 49185430: ANTHROPIC_API_KEY is not set (first seen 2026-08-07)

- [7a510dfb566b] `editor`: LLM call failed for 49151734: ANTHROPIC_API_KEY is not set (first seen 2026-08-07)

- [fc67e94da81e] `editor`: LLM call failed for 49189234: ANTHROPIC_API_KEY is not set (first seen 2026-08-07)

- [e2b0d669fbae] `editor`: LLM call failed for 49151991: ANTHROPIC_API_KEY is not set (first seen 2026-08-07)

- [b71b59cfc15c] `editor`: LLM call failed for 49187256: ANTHROPIC_API_KEY is not set (first seen 2026-08-07)

- [c1a41ea75455] `editor`: LLM call failed for 49181099: ANTHROPIC_API_KEY is not set (first seen 2026-08-07)

- [112d9ae5a151] `editor`: LLM call failed for 49185983: ANTHROPIC_API_KEY is not set (first seen 2026-08-07)

- [2b78dd9013d9] `editor`: LLM call failed for 49161518: ANTHROPIC_API_KEY is not set (first seen 2026-08-07)

- [09ccd3fa1fc3] `editor`: LLM call failed for 49187575: ANTHROPIC_API_KEY is not set (first seen 2026-08-07)

- [2681561f33ac] `editor`: LLM call failed for 49186762: ANTHROPIC_API_KEY is not set (first seen 2026-08-07)

- [cce3416a82a9] `editor`: LLM call failed for 49189287: ANTHROPIC_API_KEY is not set (first seen 2026-08-07)

- [a6fe921afb4b] `editor`: LLM call failed for 49187061: ANTHROPIC_API_KEY is not set (first seen 2026-08-07)

- [ca5b0461fff8] `editor`: LLM call failed for 49105978: ANTHROPIC_API_KEY is not set (first seen 2026-08-07)

- [f3bbba2132d7] `editor`: LLM call failed for 49200652: ANTHROPIC_API_KEY is not set (first seen 2026-08-07)

- [a0cc8bad94cf] `editor`: LLM call failed for 49096439: ANTHROPIC_API_KEY is not set (first seen 2026-08-07)

- [536198e7c0f1] `editor`: LLM call failed for 49188022: ANTHROPIC_API_KEY is not set (first seen 2026-08-07)

- [0d43894fff3b] `editor`: LLM call failed for 49162653: ANTHROPIC_API_KEY is not set (first seen 2026-08-07)

- [a8d267e97ef4] `editor`: LLM call failed for 49168622: ANTHROPIC_API_KEY is not set (first seen 2026-08-07)

- [969f9a294a57] `editor`: LLM call failed for 49120149: ANTHROPIC_API_KEY is not set (first seen 2026-08-07)

- [28b2795726d3] `editor`: LLM call failed for 49198069: ANTHROPIC_API_KEY is not set (first seen 2026-08-07)

- [9fa6898f3c84] `editor`: LLM call failed for 49184755: ANTHROPIC_API_KEY is not set (first seen 2026-08-07)

- [3f8f47816b9e] `editor`: LLM call failed for 49201003: ANTHROPIC_API_KEY is not set (first seen 2026-08-07)

- [6f0053a9cd48] `editor`: LLM call failed for 49195468: ANTHROPIC_API_KEY is not set (first seen 2026-08-07)

- [29e3e28c4bd1] `editor`: LLM call failed for 49192566: ANTHROPIC_API_KEY is not set (first seen 2026-08-07)

- [aaeb17c307de] `editor`: LLM call failed for 49184960: ANTHROPIC_API_KEY is not set (first seen 2026-08-07)

- [9b187e3da2d9] `editor`: LLM call failed for 49152255: ANTHROPIC_API_KEY is not set (first seen 2026-08-07)

- [39388a11c572] `editor`: LLM call failed for 49199357: ANTHROPIC_API_KEY is not set (first seen 2026-08-07)

- [ed2663899c85] `editor`: LLM call failed for 49201930: ANTHROPIC_API_KEY is not set (first seen 2026-08-07)

- [f82173097bb6] `editor`: LLM call failed for 49184355: ANTHROPIC_API_KEY is not set (first seen 2026-08-07)

- [677d5ac1751f] `editor`: LLM call failed for 49208314: ANTHROPIC_API_KEY is not set (first seen 2026-08-07)

- [0bb49821a5f0] `editor`: LLM call failed for 49202716: ANTHROPIC_API_KEY is not set (first seen 2026-08-07)

- [43963623eca6] `editor`: LLM call failed for 49195231: ANTHROPIC_API_KEY is not set (first seen 2026-08-07)

- [049f2fb5c76c] `editor`: LLM call failed for 49199346: ANTHROPIC_API_KEY is not set (first seen 2026-08-07)

- [59ff893453fc] `editor`: LLM call failed for 49203105: ANTHROPIC_API_KEY is not set (first seen 2026-08-07)

- [b2f5df12d5c3] `editor`: LLM call failed for 49198464: ANTHROPIC_API_KEY is not set (first seen 2026-08-07)

- [b03fec1f272b] `editor`: LLM call failed for 49204352: ANTHROPIC_API_KEY is not set (first seen 2026-08-07)

- [b52b6c4ac4c9] `editor`: LLM call failed for 49138446: ANTHROPIC_API_KEY is not set (first seen 2026-08-07)

- [37730344e5a8] `editor`: LLM call failed for 49201970: ANTHROPIC_API_KEY is not set (first seen 2026-08-07)

- [50765471a25f] `editor`: LLM call failed for 49208535: ANTHROPIC_API_KEY is not set (first seen 2026-08-07)

- [befba991a9cc] `editor`: LLM call failed for 49214863: ANTHROPIC_API_KEY is not set (first seen 2026-08-07)

- [3fe95e39babf] `editor`: LLM call failed for 49213754: ANTHROPIC_API_KEY is not set (first seen 2026-08-07)

- [535f9480dce4] `editor`: LLM call failed for 49209539: ANTHROPIC_API_KEY is not set (first seen 2026-08-07)

- [9cf66d8c49da] `editor`: LLM call failed for 49214008: ANTHROPIC_API_KEY is not set (first seen 2026-08-07)

- [af8378cbe8cf] `editor`: LLM call failed for 49214098: ANTHROPIC_API_KEY is not set (first seen 2026-08-07)

- [72ccede6d5b0] `extractor`: bot-block page detected: https://blog.cloudflare.com/cloudflare-os/ (first seen 2026-08-07)

- [4a7945681c86] `extractor`: bot-blocked (403): https://weli.dev/blog/the-valley-of-webhooks/ (first seen 2026-08-07)

- [14ae596c15d4] `extractor`: bot-block page detected: https://www.githubstatus.com/incidents/qcvjkzcs7j74 (first seen 2026-08-07)

- [086eb2d4187f] `extractor`: bot-blocked (403): https://patronview.com/news/99-percent-of-my-website-traffic-is-bots/ (first seen 2026-08-07)

- [99d095ddd6bd] `scraper.reddit`: Error - Unreachable r/SaaS: 403 Client Error: Blocked for url: https://www.reddit.com/r/SaaS/hot.json?limit=50 (first seen 2026-08-07)

- [5a75b15b8044] `scraper.reddit`: Error - Unreachable r/MachineLearning: 403 Client Error: Blocked for url: https://www.reddit.com/r/MachineLearning/hot.json?limit=50 (first seen 2026-08-07)

- [5587b61e54d7] `scraper.reddit`: Error - Unreachable r/artificial: 403 Client Error: Blocked for url: https://www.reddit.com/r/artificial/hot.json?limit=50 (first seen 2026-08-07)

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

