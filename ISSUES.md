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
- [6fe8ea9f4b2f] `editor`: LLM call failed for 49523720: ANTHROPIC_API_KEY is not set (first seen 2026-09-03)

- [a74ee1b6ff3b] `editor`: LLM call failed for 49524447: ANTHROPIC_API_KEY is not set (first seen 2026-09-03)

- [8a3da313d8fd] `editor`: LLM call failed for 49527573: ANTHROPIC_API_KEY is not set (first seen 2026-09-03)

- [cf07092d7ecb] `editor`: LLM call failed for 49522897: ANTHROPIC_API_KEY is not set (first seen 2026-09-03)

- [d9530dc68d2b] `editor`: LLM call failed for 49525297: ANTHROPIC_API_KEY is not set (first seen 2026-09-03)

- [60e5bf422844] `editor`: LLM call failed for 49523387: ANTHROPIC_API_KEY is not set (first seen 2026-09-03)

- [fe288fbb0f4d] `editor`: LLM call failed for 49524320: ANTHROPIC_API_KEY is not set (first seen 2026-09-03)

- [1e2ac6e06215] `editor`: LLM call failed for 49516059: ANTHROPIC_API_KEY is not set (first seen 2026-09-03)

- [2b362eb71e2f] `editor`: LLM call failed for 49530989: ANTHROPIC_API_KEY is not set (first seen 2026-09-03)

- [bd19c04cc8dc] `editor`: LLM call failed for 49535526: ANTHROPIC_API_KEY is not set (first seen 2026-09-03)

- [04564d90a753] `editor`: LLM call failed for 49525160: ANTHROPIC_API_KEY is not set (first seen 2026-09-03)

- [54de52fa600f] `editor`: LLM call failed for 49529621: ANTHROPIC_API_KEY is not set (first seen 2026-09-03)

- [c03a0c5751e2] `editor`: LLM call failed for 49482099: ANTHROPIC_API_KEY is not set (first seen 2026-09-03)

- [a4e6ba06b343] `editor`: LLM call failed for 49529132: ANTHROPIC_API_KEY is not set (first seen 2026-09-03)

- [4bb4da625b7c] `editor`: LLM call failed for 49524863: ANTHROPIC_API_KEY is not set (first seen 2026-09-03)

- [7683364f3ac0] `editor`: LLM call failed for 49533497: ANTHROPIC_API_KEY is not set (first seen 2026-09-03)

- [60dfd2c56b39] `editor`: LLM call failed for 49539872: ANTHROPIC_API_KEY is not set (first seen 2026-09-03)

- [61dba92c948a] `editor`: LLM call failed for 49535752: ANTHROPIC_API_KEY is not set (first seen 2026-09-03)

- [b57317b9f510] `editor`: LLM call failed for 49531651: ANTHROPIC_API_KEY is not set (first seen 2026-09-03)

- [5bad7c037f95] `editor`: LLM call failed for 49536606: ANTHROPIC_API_KEY is not set (first seen 2026-09-03)

- [468ba2f849a7] `editor`: LLM call failed for 49535548: ANTHROPIC_API_KEY is not set (first seen 2026-09-03)

- [ccbac87d532c] `editor`: LLM call failed for 49541256: ANTHROPIC_API_KEY is not set (first seen 2026-09-03)

- [cf9a4d9e56ae] `editor`: LLM call failed for 49535284: ANTHROPIC_API_KEY is not set (first seen 2026-09-03)

- [09666e11a7fd] `editor`: LLM call failed for 49536375: ANTHROPIC_API_KEY is not set (first seen 2026-09-03)

- [f4aaeed52d50] `editor`: LLM call failed for 49537553: ANTHROPIC_API_KEY is not set (first seen 2026-09-03)

- [0daad3d6c915] `extractor`: bot-blocked (403): https://www.science.org/content/article/world-s-biggest-dark-matter-detector-spots-single-weird-particle (first seen 2026-09-03)

- [3e79d52f2010] `extractor`: bot-blocked (403): https://www.nytimes.com/2026/09/02/technology/google-ad-tech-remedies.html (first seen 2026-09-03)

- [9b5f55fcee03] `editor`: LLM call failed for 49506182: ANTHROPIC_API_KEY is not set (first seen 2026-09-02)

- [0d3fb5057b22] `editor`: LLM call failed for 49510000: ANTHROPIC_API_KEY is not set (first seen 2026-09-02)

- [afb1a291584e] `editor`: LLM call failed for 49504905: ANTHROPIC_API_KEY is not set (first seen 2026-09-02)

- [8b4c79821c55] `editor`: LLM call failed for 49489376: ANTHROPIC_API_KEY is not set (first seen 2026-09-02)

- [15bed3992350] `editor`: LLM call failed for 49476239: ANTHROPIC_API_KEY is not set (first seen 2026-09-02)

- [9bc342f54616] `editor`: LLM call failed for 49515830: ANTHROPIC_API_KEY is not set (first seen 2026-09-02)

- [4295ab93c9a5] `editor`: LLM call failed for 49512975: ANTHROPIC_API_KEY is not set (first seen 2026-09-02)

- [3cf6ce5b18b1] `editor`: LLM call failed for 49516199: ANTHROPIC_API_KEY is not set (first seen 2026-09-02)

- [fa718f4f1140] `editor`: LLM call failed for 49503521: ANTHROPIC_API_KEY is not set (first seen 2026-09-02)

- [8fad3296b43d] `editor`: LLM call failed for 49517584: ANTHROPIC_API_KEY is not set (first seen 2026-09-02)

- [efdc987f85df] `editor`: LLM call failed for 49496292: ANTHROPIC_API_KEY is not set (first seen 2026-09-02)

- [ccc0db9a3234] `editor`: LLM call failed for 49511534: ANTHROPIC_API_KEY is not set (first seen 2026-09-02)

- [7d4b120486d6] `editor`: LLM call failed for 49467700: ANTHROPIC_API_KEY is not set (first seen 2026-09-02)

- [0d3de8bca6c5] `editor`: LLM call failed for 49517448: ANTHROPIC_API_KEY is not set (first seen 2026-09-02)

- [fe0116425e63] `editor`: LLM call failed for 49517624: ANTHROPIC_API_KEY is not set (first seen 2026-09-02)

- [8144481d1b6f] `editor`: LLM call failed for 49523754: ANTHROPIC_API_KEY is not set (first seen 2026-09-02)

- [6b70b231dbf5] `editor`: LLM call failed for 49493468: ANTHROPIC_API_KEY is not set (first seen 2026-09-02)

- [d67626884ecd] `editor`: LLM call failed for 49519939: ANTHROPIC_API_KEY is not set (first seen 2026-09-02)

- [f43b1799608f] `editor`: LLM call failed for 49526069: ANTHROPIC_API_KEY is not set (first seen 2026-09-02)

- [8bd32ec0ff63] `editor`: LLM call failed for 49520022: ANTHROPIC_API_KEY is not set (first seen 2026-09-02)

- [6cd6cdb9cb82] `editor`: LLM call failed for 49527396: ANTHROPIC_API_KEY is not set (first seen 2026-09-02)

- [36e9471761ed] `editor`: LLM call failed for 49521973: ANTHROPIC_API_KEY is not set (first seen 2026-09-02)

- [1d3b5bb14e1e] `editor`: LLM call failed for 49525378: ANTHROPIC_API_KEY is not set (first seen 2026-09-02)

- [e263c234a849] `editor`: LLM call failed for 49527748: ANTHROPIC_API_KEY is not set (first seen 2026-09-02)

- [fba0dd8e1f36] `extractor`: HTTP 401 for https://www.wsj.com/tech/gps-jammers-dead-zones-e76f3261 (first seen 2026-09-02)

- [d6a2af2eba0f] `extractor`: bot-blocked (403): https://garvvee.substack.com/p/no-country-for-mediocre-mathematicians (first seen 2026-09-02)

- [5548bcf3b610] `editor`: LLM call failed for 49498201: ANTHROPIC_API_KEY is not set (first seen 2026-09-01)

- [f58c058146dc] `editor`: LLM call failed for 49496782: ANTHROPIC_API_KEY is not set (first seen 2026-09-01)

- [eab1e2d2481e] `editor`: LLM call failed for 49478426: ANTHROPIC_API_KEY is not set (first seen 2026-09-01)

- [218cf3c9eace] `editor`: LLM call failed for 49480091: ANTHROPIC_API_KEY is not set (first seen 2026-09-01)

- [788d3f204b8c] `editor`: LLM call failed for 49504625: ANTHROPIC_API_KEY is not set (first seen 2026-09-01)

- [16d624a04062] `editor`: LLM call failed for 49505219: ANTHROPIC_API_KEY is not set (first seen 2026-09-01)

- [9b8e8f785053] `editor`: LLM call failed for 49503601: ANTHROPIC_API_KEY is not set (first seen 2026-09-01)

- [93efd71d4aeb] `editor`: LLM call failed for 49506142: ANTHROPIC_API_KEY is not set (first seen 2026-09-01)

- [379a166488eb] `editor`: LLM call failed for 49481141: ANTHROPIC_API_KEY is not set (first seen 2026-09-01)

- [2d3df125c489] `editor`: LLM call failed for 49506819: ANTHROPIC_API_KEY is not set (first seen 2026-09-01)

- [2b2834699559] `editor`: LLM call failed for 49507822: ANTHROPIC_API_KEY is not set (first seen 2026-09-01)

- [e7b6583c2325] `editor`: LLM call failed for 49467636: ANTHROPIC_API_KEY is not set (first seen 2026-09-01)

- [7a0f9440a89d] `editor`: LLM call failed for 49508982: ANTHROPIC_API_KEY is not set (first seen 2026-09-01)

- [187e0260d31d] `editor`: LLM call failed for 49510514: ANTHROPIC_API_KEY is not set (first seen 2026-09-01)

- [facf7890df73] `editor`: LLM call failed for 49511856: ANTHROPIC_API_KEY is not set (first seen 2026-09-01)

- [046e6ddbec82] `extractor`: bot-blocked (403): https://arstechnica.com/gaming/2026/08/a-12tb-steam-teraleak-spills-more-than-a-decade-of-lost-pc-gaming-history/ (first seen 2026-09-01)

- [68e5564046e8] `extractor`: bot-blocked (403): https://signalandsilence.substack.com/p/i-think-someone-hacked-the-commissary (first seen 2026-09-01)

- [85ff90d6eb76] `extractor`: bot-blocked (403): https://webiterate.dev/google-removed-extensions-ublock-origin-108/ (first seen 2026-09-01)

- [2cef10abac7c] `editor`: LLM call failed for 49498095: ANTHROPIC_API_KEY is not set (first seen 2026-08-31)

- [3716d2340c77] `editor`: LLM call failed for 49497063: ANTHROPIC_API_KEY is not set (first seen 2026-08-31)

- [07afadb59f0c] `editor`: LLM call failed for 49426995: ANTHROPIC_API_KEY is not set (first seen 2026-08-31)

- [b888ecc67a53] `editor`: LLM call failed for 49490870: ANTHROPIC_API_KEY is not set (first seen 2026-08-31)

- [da0903ca03b6] `editor`: LLM call failed for 49494182: ANTHROPIC_API_KEY is not set (first seen 2026-08-31)

- [727563292385] `editor`: LLM call failed for 49492632: ANTHROPIC_API_KEY is not set (first seen 2026-08-31)

- [d4196de080e9] `editor`: LLM call failed for 49425252: ANTHROPIC_API_KEY is not set (first seen 2026-08-31)

- [ceed1fe1de72] `editor`: LLM call failed for 49494520: ANTHROPIC_API_KEY is not set (first seen 2026-08-31)

- [b54f79bac9a4] `editor`: LLM call failed for 49494301: ANTHROPIC_API_KEY is not set (first seen 2026-08-31)

- [2388b974e7bf] `editor`: LLM call failed for 49463888: ANTHROPIC_API_KEY is not set (first seen 2026-08-31)

- [bfb34bf5eed6] `editor`: LLM call failed for 49495372: ANTHROPIC_API_KEY is not set (first seen 2026-08-31)

- [1995c651420a] `editor`: LLM call failed for 49498787: ANTHROPIC_API_KEY is not set (first seen 2026-08-31)

- [75f82601d5d8] `editor`: LLM call failed for 49498978: ANTHROPIC_API_KEY is not set (first seen 2026-08-31)

- [277f7edd68f1] `editor`: LLM call failed for 49499854: ANTHROPIC_API_KEY is not set (first seen 2026-08-31)

- [a5af74336d04] `editor`: LLM call failed for 49499394: ANTHROPIC_API_KEY is not set (first seen 2026-08-31)

- [426596e0cfc6] `editor`: LLM call failed for 49496918: ANTHROPIC_API_KEY is not set (first seen 2026-08-31)

- [a49eec0145a3] `editor`: LLM call failed for 49499867: ANTHROPIC_API_KEY is not set (first seen 2026-08-31)

- [00b0dbfa427c] `editor`: LLM call failed for 49491791: ANTHROPIC_API_KEY is not set (first seen 2026-08-31)

- [1c139be7425a] `editor`: LLM call failed for 49497810: ANTHROPIC_API_KEY is not set (first seen 2026-08-31)

- [9aa6470e633f] `editor`: LLM call failed for 49489057: ANTHROPIC_API_KEY is not set (first seen 2026-08-30)

- [012745927cf7] `editor`: LLM call failed for 49489982: ANTHROPIC_API_KEY is not set (first seen 2026-08-30)

- [7545b74d6970] `editor`: LLM call failed for 49492193: ANTHROPIC_API_KEY is not set (first seen 2026-08-30)

- [ae4c54b9a5a6] `editor`: LLM call failed for 49477212: ANTHROPIC_API_KEY is not set (first seen 2026-08-30)

- [cb84c2314f75] `editor`: LLM call failed for 49479924: ANTHROPIC_API_KEY is not set (first seen 2026-08-30)

- [a51019f30023] `editor`: LLM call failed for 49486172: ANTHROPIC_API_KEY is not set (first seen 2026-08-30)

- [499c610f8a33] `editor`: LLM call failed for 49490702: ANTHROPIC_API_KEY is not set (first seen 2026-08-30)

- [3716b0b8b50d] `editor`: LLM call failed for 49485416: ANTHROPIC_API_KEY is not set (first seen 2026-08-30)

- [a1abf084aa01] `editor`: LLM call failed for 49485267: ANTHROPIC_API_KEY is not set (first seen 2026-08-30)

- [5f72ad9f8afb] `editor`: LLM call failed for 49486081: ANTHROPIC_API_KEY is not set (first seen 2026-08-30)

- [a1d8dda52dfd] `editor`: LLM call failed for 49487341: ANTHROPIC_API_KEY is not set (first seen 2026-08-30)

- [4ee320f65e10] `editor`: LLM call failed for 49491568: ANTHROPIC_API_KEY is not set (first seen 2026-08-30)

- [65c87b675955] `editor`: LLM call failed for 49492219: ANTHROPIC_API_KEY is not set (first seen 2026-08-30)

- [349c1dbec645] `editor`: LLM call failed for 49433328: ANTHROPIC_API_KEY is not set (first seen 2026-08-30)

- [b1485b323556] `editor`: LLM call failed for 49424320: ANTHROPIC_API_KEY is not set (first seen 2026-08-30)

- [1cb47742ea22] `editor`: LLM call failed for 49415386: ANTHROPIC_API_KEY is not set (first seen 2026-08-30)

- [31ef75675918] `editor`: LLM call failed for 49478103: ANTHROPIC_API_KEY is not set (first seen 2026-08-29)

- [e0679f3277ee] `editor`: LLM call failed for 49471407: ANTHROPIC_API_KEY is not set (first seen 2026-08-29)

- [c69d19ae9f34] `editor`: LLM call failed for 49471965: ANTHROPIC_API_KEY is not set (first seen 2026-08-29)

- [a446bd5b07f3] `editor`: LLM call failed for 49474786: ANTHROPIC_API_KEY is not set (first seen 2026-08-29)

- [68e870c7e796] `editor`: LLM call failed for 49476143: ANTHROPIC_API_KEY is not set (first seen 2026-08-29)

- [3538f0597389] `editor`: LLM call failed for 49475079: ANTHROPIC_API_KEY is not set (first seen 2026-08-29)

- [259fa3eba4a2] `editor`: LLM call failed for 49472090: ANTHROPIC_API_KEY is not set (first seen 2026-08-29)

- [e2a994070d9e] `editor`: LLM call failed for 49477600: ANTHROPIC_API_KEY is not set (first seen 2026-08-29)

- [887bfe6da25e] `editor`: LLM call failed for 49478340: ANTHROPIC_API_KEY is not set (first seen 2026-08-29)

- [5ca858eae805] `editor`: LLM call failed for 49479878: ANTHROPIC_API_KEY is not set (first seen 2026-08-29)

- [3415c6d5e4bb] `editor`: LLM call failed for 49472216: ANTHROPIC_API_KEY is not set (first seen 2026-08-29)

- [8c9fa1bc7cfe] `editor`: LLM call failed for 49480466: ANTHROPIC_API_KEY is not set (first seen 2026-08-29)

- [00f5b73eac36] `editor`: LLM call failed for 49477854: ANTHROPIC_API_KEY is not set (first seen 2026-08-29)

- [fbbdce4db3cc] `editor`: LLM call failed for 49477564: ANTHROPIC_API_KEY is not set (first seen 2026-08-29)

- [9bac6281679f] `editor`: LLM call failed for 49479837: ANTHROPIC_API_KEY is not set (first seen 2026-08-29)

- [8813d78628fe] `editor`: LLM call failed for 49478178: ANTHROPIC_API_KEY is not set (first seen 2026-08-29)

- [c8607ad35d8b] `editor`: LLM call failed for 49464391: ANTHROPIC_API_KEY is not set (first seen 2026-08-28)

- [1a477ac6d692] `editor`: LLM call failed for 49456929: ANTHROPIC_API_KEY is not set (first seen 2026-08-28)

- [73db791d6a89] `editor`: LLM call failed for 49452346: ANTHROPIC_API_KEY is not set (first seen 2026-08-28)

- [64467423f2fd] `editor`: LLM call failed for 49451675: ANTHROPIC_API_KEY is not set (first seen 2026-08-28)

- [b090e4d516f5] `editor`: LLM call failed for 49455956: ANTHROPIC_API_KEY is not set (first seen 2026-08-28)

- [7421497d996c] `editor`: LLM call failed for 49462253: ANTHROPIC_API_KEY is not set (first seen 2026-08-28)

- [5e1ed02cf047] `editor`: LLM call failed for 49453161: ANTHROPIC_API_KEY is not set (first seen 2026-08-28)

- [0041a899398e] `editor`: LLM call failed for 49456851: ANTHROPIC_API_KEY is not set (first seen 2026-08-28)

- [a4bc2373c26c] `editor`: LLM call failed for 49450898: ANTHROPIC_API_KEY is not set (first seen 2026-08-28)

- [0440da4133b3] `editor`: LLM call failed for 49457545: ANTHROPIC_API_KEY is not set (first seen 2026-08-28)

- [983afefb83b2] `editor`: LLM call failed for 49458418: ANTHROPIC_API_KEY is not set (first seen 2026-08-28)

- [2488cec7a933] `editor`: LLM call failed for 49464896: ANTHROPIC_API_KEY is not set (first seen 2026-08-28)

- [b6955b2b0249] `editor`: LLM call failed for 49457512: ANTHROPIC_API_KEY is not set (first seen 2026-08-28)

- [7af872c674df] `editor`: LLM call failed for 49467922: ANTHROPIC_API_KEY is not set (first seen 2026-08-28)

- [409174aea83e] `editor`: LLM call failed for 49466894: ANTHROPIC_API_KEY is not set (first seen 2026-08-28)

- [6d186e871254] `editor`: LLM call failed for 49466006: ANTHROPIC_API_KEY is not set (first seen 2026-08-28)

- [cb6f4fbdd689] `editor`: LLM call failed for 49468642: ANTHROPIC_API_KEY is not set (first seen 2026-08-28)

- [dcea7e9eb279] `editor`: LLM call failed for 49461817: ANTHROPIC_API_KEY is not set (first seen 2026-08-28)

- [c0814eabd911] `editor`: LLM call failed for 49468818: ANTHROPIC_API_KEY is not set (first seen 2026-08-28)

- [081f59973dc9] `editor`: LLM call failed for 49465169: ANTHROPIC_API_KEY is not set (first seen 2026-08-28)

- [7692fc83d808] `editor`: LLM call failed for 49466917: ANTHROPIC_API_KEY is not set (first seen 2026-08-28)

- [cb4bac0f0385] `editor`: LLM call failed for 49462763: ANTHROPIC_API_KEY is not set (first seen 2026-08-28)

- [feeae3fd0cde] `extractor`: bot-blocked (403): https://www.nytimes.com/2026/08/26/arts/yayoi-kusama-dead.html (first seen 2026-08-28)

- [332e1d5ea2f1] `extractor`: bot-blocked (403): https://www.gatesnotes.com/a-turbulent-ai-era-and-critical-choices-to-make (first seen 2026-08-28)

- [5ffe33d026d1] `extractor`: bot-blocked (403): https://www.gatesnotes.com/work/make-ai-work-for-everyone/reader/a-turbulent-ai-era-and-critical-choices-to-make?WT.mc_id=20260826_ai-overture-2026-med-med (first seen 2026-08-28)

- [1df4bde2f5e1] `extractor`: bot-blocked (403): https://www.nytimes.com/2026/08/27/technology/anthropic-government-blacklisting-ruling.html (first seen 2026-08-28)

- [c9282f4ae630] `extractor`: bot-block page detected: https://blog.cloudflare.com/dns-cache-memory-optimization-1111/ (first seen 2026-08-28)

- [315984f81eac] `editor`: LLM call failed for 49437483: ANTHROPIC_API_KEY is not set (first seen 2026-08-27)

- [8929a5dd84c7] `editor`: LLM call failed for 49436786: ANTHROPIC_API_KEY is not set (first seen 2026-08-27)

- [3a47597b6626] `editor`: LLM call failed for 49437210: ANTHROPIC_API_KEY is not set (first seen 2026-08-27)

- [2c33c4eed8c0] `editor`: LLM call failed for 49411800: ANTHROPIC_API_KEY is not set (first seen 2026-08-27)

- [da370bab8cc7] `editor`: LLM call failed for 49432201: ANTHROPIC_API_KEY is not set (first seen 2026-08-27)

- [b09b76c137a7] `editor`: LLM call failed for 49439017: ANTHROPIC_API_KEY is not set (first seen 2026-08-27)

- [43dd23f60c94] `editor`: LLM call failed for 49442589: ANTHROPIC_API_KEY is not set (first seen 2026-08-27)

- [7f7da7a397df] `editor`: LLM call failed for 49445727: ANTHROPIC_API_KEY is not set (first seen 2026-08-27)

- [adde6a90d772] `editor`: LLM call failed for 49451448: ANTHROPIC_API_KEY is not set (first seen 2026-08-27)

- [83c263061543] `editor`: LLM call failed for 49450448: ANTHROPIC_API_KEY is not set (first seen 2026-08-27)

- [31c42fda0862] `editor`: LLM call failed for 49449749: ANTHROPIC_API_KEY is not set (first seen 2026-08-27)

- [3fb3d3c5a858] `editor`: LLM call failed for 49454728: ANTHROPIC_API_KEY is not set (first seen 2026-08-27)

- [4b13d7d537b6] `editor`: LLM call failed for 49452671: ANTHROPIC_API_KEY is not set (first seen 2026-08-27)

- [b217db5c337d] `editor`: LLM call failed for 49454314: ANTHROPIC_API_KEY is not set (first seen 2026-08-27)

- [a59bf55a926d] `editor`: LLM call failed for 49449576: ANTHROPIC_API_KEY is not set (first seen 2026-08-27)

- [fef051b32889] `editor`: LLM call failed for 49458161: ANTHROPIC_API_KEY is not set (first seen 2026-08-27)

- [ae4aead61f2d] `editor`: LLM call failed for 49448210: ANTHROPIC_API_KEY is not set (first seen 2026-08-27)

- [2291a48e82ae] `editor`: LLM call failed for 49452980: ANTHROPIC_API_KEY is not set (first seen 2026-08-27)

- [b07c0c511999] `editor`: LLM call failed for 49448321: ANTHROPIC_API_KEY is not set (first seen 2026-08-27)

- [a128d6006ec5] `editor`: LLM call failed for 49452990: ANTHROPIC_API_KEY is not set (first seen 2026-08-27)

- [5004b4d46ddd] `extractor`: bot-blocked (403): https://www.bloomberg.com/news/articles/2026-08-26/china-s-z-ai-made-ox-alpha-stealth-model-that-rivals-deepseek (first seen 2026-08-27)

- [f6f501eccaf9] `extractor`: bot-block page detected: https://www.githubstatus.com/incidents/hcbtzksccj2f (first seen 2026-08-27)

- [39c081572e6b] `extractor`: HTTP 401 for https://www.reuters.com/world/us/meta-settles-with-us-states-over-social-media-harms-2026-08-26/ (first seen 2026-08-27)

- [94105de5ed34] `extractor`: HTTP 401 for https://www.wsj.com/politics/policy/u-s-state-department-pauses-immigrant-visa-applications-25b31b23 (first seen 2026-08-27)

- [70bc445798e5] `extractor`: empty body extracted: https://z.ai/blog/glm-5.3-flash (first seen 2026-08-27)

- [94ae203e68b3] `editor`: LLM call failed for 49399722: ANTHROPIC_API_KEY is not set (first seen 2026-08-25)

- [bee32f6263a2] `editor`: LLM call failed for 49420530: ANTHROPIC_API_KEY is not set (first seen 2026-08-25)

- [6d6c2485f95b] `editor`: LLM call failed for 49422800: ANTHROPIC_API_KEY is not set (first seen 2026-08-25)

- [08ef46abad43] `editor`: LLM call failed for 49419351: ANTHROPIC_API_KEY is not set (first seen 2026-08-25)

- [bab1edf5cefd] `editor`: LLM call failed for 49421536: ANTHROPIC_API_KEY is not set (first seen 2026-08-25)

- [d39349ec745a] `editor`: LLM call failed for 49426564: ANTHROPIC_API_KEY is not set (first seen 2026-08-25)

- [f98f34082d45] `editor`: LLM call failed for 49435728: ANTHROPIC_API_KEY is not set (first seen 2026-08-25)

- [9c1fb668d2c4] `editor`: LLM call failed for 49419252: ANTHROPIC_API_KEY is not set (first seen 2026-08-25)

- [406976c79c8e] `editor`: LLM call failed for 49426466: ANTHROPIC_API_KEY is not set (first seen 2026-08-25)

- [57635c01000d] `editor`: LLM call failed for 49428121: ANTHROPIC_API_KEY is not set (first seen 2026-08-25)

- [6b39e5221ca8] `editor`: LLM call failed for 49432317: ANTHROPIC_API_KEY is not set (first seen 2026-08-25)

- [b3153c06bbe7] `editor`: LLM call failed for 49437946: ANTHROPIC_API_KEY is not set (first seen 2026-08-25)

- [61be90e4847a] `editor`: LLM call failed for 49432319: ANTHROPIC_API_KEY is not set (first seen 2026-08-25)

- [e436335fa6ca] `editor`: LLM call failed for 49437069: ANTHROPIC_API_KEY is not set (first seen 2026-08-25)

- [8109524c5626] `editor`: LLM call failed for 49434645: ANTHROPIC_API_KEY is not set (first seen 2026-08-25)

- [5c79c2c72c8b] `editor`: LLM call failed for 49437283: ANTHROPIC_API_KEY is not set (first seen 2026-08-25)

- [42dc75349e41] `editor`: LLM call failed for 49433292: ANTHROPIC_API_KEY is not set (first seen 2026-08-25)

- [73f748a3ad98] `editor`: LLM call failed for 49433450: ANTHROPIC_API_KEY is not set (first seen 2026-08-25)

- [e72f22c76582] `editor`: LLM call failed for 49434820: ANTHROPIC_API_KEY is not set (first seen 2026-08-25)

- [dfd239991ff2] `editor`: LLM call failed for 49438052: ANTHROPIC_API_KEY is not set (first seen 2026-08-25)

- [6cc0ae888517] `editor`: LLM call failed for 49433316: ANTHROPIC_API_KEY is not set (first seen 2026-08-25)

- [3e86844591cb] `editor`: LLM call failed for 49434378: ANTHROPIC_API_KEY is not set (first seen 2026-08-25)

- [a6be78191ba1] `editor`: LLM call failed for 49411395: ANTHROPIC_API_KEY is not set (first seen 2026-08-24)

- [5b0dd60691dd] `editor`: LLM call failed for 49410932: ANTHROPIC_API_KEY is not set (first seen 2026-08-24)

- [3afd6996eb93] `editor`: LLM call failed for 49411717: ANTHROPIC_API_KEY is not set (first seen 2026-08-24)

- [dbb639b31afa] `editor`: LLM call failed for 49415621: ANTHROPIC_API_KEY is not set (first seen 2026-08-24)

- [2a342dbef967] `editor`: LLM call failed for 49411468: ANTHROPIC_API_KEY is not set (first seen 2026-08-24)

- [4e405e116c9e] `editor`: LLM call failed for 49420902: ANTHROPIC_API_KEY is not set (first seen 2026-08-24)

- [bc2d1cdd7f0d] `editor`: LLM call failed for 49416055: ANTHROPIC_API_KEY is not set (first seen 2026-08-24)

- [effb7f39776a] `editor`: LLM call failed for 49411102: ANTHROPIC_API_KEY is not set (first seen 2026-08-24)

- [f4795e6fd2b5] `editor`: LLM call failed for 49413561: ANTHROPIC_API_KEY is not set (first seen 2026-08-24)

- [27e6576473c2] `editor`: LLM call failed for 49413320: ANTHROPIC_API_KEY is not set (first seen 2026-08-24)

- [bd20a2528e80] `editor`: LLM call failed for 49412396: ANTHROPIC_API_KEY is not set (first seen 2026-08-24)

- [9996904e9de8] `editor`: LLM call failed for 49421554: ANTHROPIC_API_KEY is not set (first seen 2026-08-24)

- [8649f0b6afb1] `editor`: LLM call failed for 49415271: ANTHROPIC_API_KEY is not set (first seen 2026-08-24)

- [eef48105ed51] `editor`: LLM call failed for 49421074: ANTHROPIC_API_KEY is not set (first seen 2026-08-24)

- [b316e382182d] `editor`: LLM call failed for 49424606: ANTHROPIC_API_KEY is not set (first seen 2026-08-24)

- [1657e674a1c1] `editor`: LLM call failed for 49421489: ANTHROPIC_API_KEY is not set (first seen 2026-08-24)

- [8fce54bd6814] `editor`: LLM call failed for 49422784: ANTHROPIC_API_KEY is not set (first seen 2026-08-24)

- [cb47fbbea878] `editor`: LLM call failed for 49419237: ANTHROPIC_API_KEY is not set (first seen 2026-08-24)

- [e4e14e4fdab0] `editor`: LLM call failed for 49420873: ANTHROPIC_API_KEY is not set (first seen 2026-08-24)

- [e1c707455b44] `editor`: LLM call failed for 49421158: ANTHROPIC_API_KEY is not set (first seen 2026-08-24)

- [a498cd9f75ae] `extractor`: bot-blocked (403): https://bookdna.com/best-books/nonfiction-about-cults-scams-and-schemes (first seen 2026-08-24)

- [8eb3f329251a] `extractor`: bot-block page detected: https://securelist.com/android-head-unit-malware/121106/ (first seen 2026-08-24)

- [a69844161e8a] `editor`: LLM call failed for 49401549: ANTHROPIC_API_KEY is not set (first seen 2026-08-23)

- [ff6521bf208e] `editor`: LLM call failed for 49393051: ANTHROPIC_API_KEY is not set (first seen 2026-08-23)

- [81597b531ed3] `editor`: LLM call failed for 49355659: ANTHROPIC_API_KEY is not set (first seen 2026-08-23)

- [992872593c54] `editor`: LLM call failed for 49399591: ANTHROPIC_API_KEY is not set (first seen 2026-08-23)

- [8b6463bce7ed] `editor`: LLM call failed for 49402202: ANTHROPIC_API_KEY is not set (first seen 2026-08-23)

- [c5928caf8aa4] `editor`: LLM call failed for 49346854: ANTHROPIC_API_KEY is not set (first seen 2026-08-23)

- [28e0dd3944da] `editor`: LLM call failed for 49399898: ANTHROPIC_API_KEY is not set (first seen 2026-08-23)

- [3f95b1c1a82a] `editor`: LLM call failed for 49351802: ANTHROPIC_API_KEY is not set (first seen 2026-08-23)

- [f9360d281c09] `editor`: LLM call failed for 49402232: ANTHROPIC_API_KEY is not set (first seen 2026-08-23)

- [dd11b3f5a5b7] `editor`: LLM call failed for 49409200: ANTHROPIC_API_KEY is not set (first seen 2026-08-23)

- [6a8339a6ee2c] `editor`: LLM call failed for 49409073: ANTHROPIC_API_KEY is not set (first seen 2026-08-23)

- [4a69eb84a3d8] `editor`: LLM call failed for 49407507: ANTHROPIC_API_KEY is not set (first seen 2026-08-23)

- [4bd8b2206b68] `editor`: LLM call failed for 49405816: ANTHROPIC_API_KEY is not set (first seen 2026-08-23)

- [16f976568b4c] `editor`: LLM call failed for 49405870: ANTHROPIC_API_KEY is not set (first seen 2026-08-23)

- [f15e875fe2d3] `editor`: LLM call failed for 49409473: ANTHROPIC_API_KEY is not set (first seen 2026-08-23)

- [7a399b34e1a1] `editor`: LLM call failed for 49406539: ANTHROPIC_API_KEY is not set (first seen 2026-08-23)

- [fc7fff4d0780] `editor`: LLM call failed for 49409092: ANTHROPIC_API_KEY is not set (first seen 2026-08-23)

- [0a0b594394d0] `editor`: LLM call failed for 49410362: ANTHROPIC_API_KEY is not set (first seen 2026-08-23)

- [ac5646e36401] `editor`: LLM call failed for 49411643: ANTHROPIC_API_KEY is not set (first seen 2026-08-23)

- [db07961e0018] `extractor`: HTTP 401 for https://www.reuters.com/world/how-texas-student-blew-whistle-rogue-ai-hacking-attempt-2026-08-20/ (first seen 2026-08-23)

- [67a6ce1bd654] `extractor`: bot-blocked (403): https://decodingvibes.com/blog/a-kantian-critique-of-sorry-by-justin-bieber/ (first seen 2026-08-23)

- [54ec8ae38a77] `editor`: LLM call failed for 49346444: ANTHROPIC_API_KEY is not set (first seen 2026-08-22)

- [49b63d12935e] `editor`: LLM call failed for 49387525: ANTHROPIC_API_KEY is not set (first seen 2026-08-22)

- [0e2a52751c73] `editor`: LLM call failed for 49388752: ANTHROPIC_API_KEY is not set (first seen 2026-08-22)

- [184e18889af7] `editor`: LLM call failed for 49394496: ANTHROPIC_API_KEY is not set (first seen 2026-08-22)

- [e6bc396dc6ec] `editor`: LLM call failed for 49391553: ANTHROPIC_API_KEY is not set (first seen 2026-08-22)

- [1e7fdc904b05] `editor`: LLM call failed for 49395628: ANTHROPIC_API_KEY is not set (first seen 2026-08-22)

- [32e1c061bc60] `editor`: LLM call failed for 49392200: ANTHROPIC_API_KEY is not set (first seen 2026-08-22)

- [6fb397fe993e] `editor`: LLM call failed for 49384210: ANTHROPIC_API_KEY is not set (first seen 2026-08-22)

- [2ac05e2dfed7] `editor`: LLM call failed for 49393052: ANTHROPIC_API_KEY is not set (first seen 2026-08-22)

- [c2094481bf20] `editor`: LLM call failed for 49398152: ANTHROPIC_API_KEY is not set (first seen 2026-08-22)

- [5ca5c3ad8578] `editor`: LLM call failed for 49397074: ANTHROPIC_API_KEY is not set (first seen 2026-08-22)

- [2b398d8a9bc7] `editor`: LLM call failed for 49400408: ANTHROPIC_API_KEY is not set (first seen 2026-08-22)

- [e32bb093c2df] `editor`: LLM call failed for 49402189: ANTHROPIC_API_KEY is not set (first seen 2026-08-22)

- [149a5d3664e4] `extractor`: HTTP 429 for https://www.felonybench.com/ (first seen 2026-08-22)

- [7f8a4a8f548a] `editor`: LLM call failed for 49375996: ANTHROPIC_API_KEY is not set (first seen 2026-08-21)

- [9d0f768112a0] `editor`: LLM call failed for 49378446: ANTHROPIC_API_KEY is not set (first seen 2026-08-21)

- [3408b62e737c] `editor`: LLM call failed for 49377853: ANTHROPIC_API_KEY is not set (first seen 2026-08-21)

- [8757cfca2496] `editor`: LLM call failed for 49378243: ANTHROPIC_API_KEY is not set (first seen 2026-08-21)

- [6497da68c918] `editor`: LLM call failed for 49378768: ANTHROPIC_API_KEY is not set (first seen 2026-08-21)

- [b332c520dfca] `editor`: LLM call failed for 49384180: ANTHROPIC_API_KEY is not set (first seen 2026-08-21)

- [896881006117] `editor`: LLM call failed for 49376265: ANTHROPIC_API_KEY is not set (first seen 2026-08-21)

- [7a879be30725] `editor`: LLM call failed for 49375719: ANTHROPIC_API_KEY is not set (first seen 2026-08-21)

- [c0f9f1a97eb1] `editor`: LLM call failed for 49360140: ANTHROPIC_API_KEY is not set (first seen 2026-08-21)

- [17b5b82f536d] `editor`: LLM call failed for 49381896: ANTHROPIC_API_KEY is not set (first seen 2026-08-21)

- [fae1a471dd47] `editor`: LLM call failed for 49385860: ANTHROPIC_API_KEY is not set (first seen 2026-08-21)

- [7476decba80f] `editor`: LLM call failed for 49387497: ANTHROPIC_API_KEY is not set (first seen 2026-08-21)

- [0a3f195c82b0] `editor`: LLM call failed for 49384896: ANTHROPIC_API_KEY is not set (first seen 2026-08-21)

- [32f0bebc4f08] `editor`: LLM call failed for 49383026: ANTHROPIC_API_KEY is not set (first seen 2026-08-21)

- [4e5b475e5289] `editor`: LLM call failed for 49386699: ANTHROPIC_API_KEY is not set (first seen 2026-08-21)

- [57c4864ddb8d] `editor`: LLM call failed for 49387570: ANTHROPIC_API_KEY is not set (first seen 2026-08-21)

- [a034c222e182] `editor`: LLM call failed for 49386163: ANTHROPIC_API_KEY is not set (first seen 2026-08-21)

- [694d934602c8] `editor`: LLM call failed for 49390427: ANTHROPIC_API_KEY is not set (first seen 2026-08-21)

- [edd6b1b9830b] `editor`: LLM call failed for 49388154: ANTHROPIC_API_KEY is not set (first seen 2026-08-21)

- [f247b543f231] `editor`: LLM call failed for 49389430: ANTHROPIC_API_KEY is not set (first seen 2026-08-21)

- [ecb541335c35] `extractor`: bot-block page detected: https://blog.laserphile.com/2026/08/aliexpress-webpage-keeping-multipoint.html (first seen 2026-08-21)

- [ef0e7cf4c233] `extractor`: bot-blocked (403): https://www.nytimes.com/2026/08/21/us/politics/samuel-tunick-deleted-phone-felony.html (first seen 2026-08-21)

- [2dc69bafae83] `extractor`: bot-blocked (403): https://www.economist.com/graphic-detail/2026/08/18/does-ai-stop-children-from-learning (first seen 2026-08-21)

- [fa4b84dde909] `editor`: LLM call failed for 49362728: ANTHROPIC_API_KEY is not set (first seen 2026-08-20)

- [8a7509bb81ab] `editor`: LLM call failed for 49353339: ANTHROPIC_API_KEY is not set (first seen 2026-08-20)

- [76b7f36950a6] `editor`: LLM call failed for 49365841: ANTHROPIC_API_KEY is not set (first seen 2026-08-20)

- [de2882c42571] `editor`: LLM call failed for 49286258: ANTHROPIC_API_KEY is not set (first seen 2026-08-20)

- [f9ad1430ebc7] `editor`: LLM call failed for 49365443: ANTHROPIC_API_KEY is not set (first seen 2026-08-20)

- [ff0afd18bf3f] `editor`: LLM call failed for 49374738: ANTHROPIC_API_KEY is not set (first seen 2026-08-20)

- [368ed616f3b2] `editor`: LLM call failed for 49362401: ANTHROPIC_API_KEY is not set (first seen 2026-08-20)

- [ac01e9e2d4d5] `editor`: LLM call failed for 49371857: ANTHROPIC_API_KEY is not set (first seen 2026-08-20)

- [aeb05f135829] `editor`: LLM call failed for 49367350: ANTHROPIC_API_KEY is not set (first seen 2026-08-20)

- [46f83a7cd815] `editor`: LLM call failed for 49348189: ANTHROPIC_API_KEY is not set (first seen 2026-08-20)

- [5781de05a295] `editor`: LLM call failed for 49323795: ANTHROPIC_API_KEY is not set (first seen 2026-08-20)

- [4ae385191591] `editor`: LLM call failed for 49374797: ANTHROPIC_API_KEY is not set (first seen 2026-08-20)

- [4ceb6d7f7301] `editor`: LLM call failed for 49369408: ANTHROPIC_API_KEY is not set (first seen 2026-08-20)

- [f7cd37883af8] `editor`: LLM call failed for 49371006: ANTHROPIC_API_KEY is not set (first seen 2026-08-20)

- [26670d428b20] `editor`: LLM call failed for 49348141: ANTHROPIC_API_KEY is not set (first seen 2026-08-20)

- [4f68c0d15e77] `editor`: LLM call failed for 49348079: ANTHROPIC_API_KEY is not set (first seen 2026-08-20)

- [bfd7b0a14508] `editor`: LLM call failed for 49373456: ANTHROPIC_API_KEY is not set (first seen 2026-08-20)

- [ea771fa926fd] `editor`: LLM call failed for 49379550: ANTHROPIC_API_KEY is not set (first seen 2026-08-20)

- [ce13cd5126dd] `editor`: LLM call failed for 49374269: ANTHROPIC_API_KEY is not set (first seen 2026-08-20)

- [c83c7b0a25fd] `editor`: LLM call failed for 49362689: ANTHROPIC_API_KEY is not set (first seen 2026-08-20)

- [0af5b9a2d637] `editor`: LLM call failed for 49347543: ANTHROPIC_API_KEY is not set (first seen 2026-08-20)

- [ec7a71e7bb37] `editor`: LLM call failed for 49378957: ANTHROPIC_API_KEY is not set (first seen 2026-08-20)

- [3277422764c8] `extractor`: bot-blocked (403): https://www.rathbiotaclan.com/tiktok-videos-deactivate-key-cognitive-brain-regions/ (first seen 2026-08-20)

- [5189ac6b3265] `extractor`: HTTP 429 for https://blog.laserphile.com/2026/08/aliexpress-webpage-keeping-multipoint.html (first seen 2026-08-20)

- [fda918d7bf0a] `extractor`: HTTP 401 for https://www.wsj.com/tech/steve-jobs-apple-next-cia-161b65f9?st=NWWds1&reflink=desktopwebshare_permalink (first seen 2026-08-20)

- [64d28e57ee51] `editor`: LLM call failed for 49351330: ANTHROPIC_API_KEY is not set (first seen 2026-08-19)

- [35ce8ec06974] `editor`: LLM call failed for 49355142: ANTHROPIC_API_KEY is not set (first seen 2026-08-19)

- [7f8731ad738d] `editor`: LLM call failed for 49348912: ANTHROPIC_API_KEY is not set (first seen 2026-08-19)

- [d515ef5800ee] `editor`: LLM call failed for 49311814: ANTHROPIC_API_KEY is not set (first seen 2026-08-19)

- [1a5d40c7c53c] `editor`: LLM call failed for 49342472: ANTHROPIC_API_KEY is not set (first seen 2026-08-19)

- [3cfa1efe111d] `editor`: LLM call failed for 49349984: ANTHROPIC_API_KEY is not set (first seen 2026-08-19)

- [374ad6891c26] `editor`: LLM call failed for 49353221: ANTHROPIC_API_KEY is not set (first seen 2026-08-19)

- [c831f65ffa8a] `editor`: LLM call failed for 49348055: ANTHROPIC_API_KEY is not set (first seen 2026-08-19)

- [bf3326993abd] `editor`: LLM call failed for 49363433: ANTHROPIC_API_KEY is not set (first seen 2026-08-19)

- [04292d7ed62f] `editor`: LLM call failed for 49358327: ANTHROPIC_API_KEY is not set (first seen 2026-08-19)

- [0fafe8266dfd] `editor`: LLM call failed for 49349898: ANTHROPIC_API_KEY is not set (first seen 2026-08-19)

- [da22e901d5ce] `editor`: LLM call failed for 49354949: ANTHROPIC_API_KEY is not set (first seen 2026-08-19)

- [8f59701d3445] `editor`: LLM call failed for 49344643: ANTHROPIC_API_KEY is not set (first seen 2026-08-19)

- [23d4715ae12d] `editor`: LLM call failed for 49306207: ANTHROPIC_API_KEY is not set (first seen 2026-08-19)

- [ed648266fc50] `editor`: LLM call failed for 49321298: ANTHROPIC_API_KEY is not set (first seen 2026-08-19)

- [34d31ce88058] `editor`: LLM call failed for 49355105: ANTHROPIC_API_KEY is not set (first seen 2026-08-19)

- [2d42c8795a81] `editor`: LLM call failed for 49355606: ANTHROPIC_API_KEY is not set (first seen 2026-08-19)

- [5931dcc5e252] `editor`: LLM call failed for 49362934: ANTHROPIC_API_KEY is not set (first seen 2026-08-19)

- [a5bb96ce0384] `editor`: LLM call failed for 49360242: ANTHROPIC_API_KEY is not set (first seen 2026-08-19)

- [f50fa3c01731] `editor`: LLM call failed for 49359425: ANTHROPIC_API_KEY is not set (first seen 2026-08-19)

- [f0ba2768bcc2] `editor`: LLM call failed for 49361395: ANTHROPIC_API_KEY is not set (first seen 2026-08-19)

- [ed6c7da3f935] `editor`: LLM call failed for 49361279: ANTHROPIC_API_KEY is not set (first seen 2026-08-19)

- [6b9dda354d96] `editor`: LLM call failed for 49360545: ANTHROPIC_API_KEY is not set (first seen 2026-08-19)

- [8ef6d97ec12c] `editor`: LLM call failed for 49364745: ANTHROPIC_API_KEY is not set (first seen 2026-08-19)

- [25c480b234df] `editor`: LLM call failed for 49360015: ANTHROPIC_API_KEY is not set (first seen 2026-08-19)

- [48f6935743fa] `editor`: LLM call failed for 49365405: ANTHROPIC_API_KEY is not set (first seen 2026-08-19)

- [c716a0b29aec] `editor`: LLM call failed for 49364559: ANTHROPIC_API_KEY is not set (first seen 2026-08-19)

- [4df0d3f58f66] `extractor`: bot-blocked (403): https://www.economist.com/business/2026/08/18/metas-blockbuster-trial-draws-parallels-to-big-tobacco (first seen 2026-08-19)

- [4a38f359d29d] `extractor`: bot-blocked (403): https://www.casio.com/uk/watches/casio/product.F-B100W-1A/ (first seen 2026-08-19)

- [212b6f765d38] `editor`: LLM call failed for 49333824: ANTHROPIC_API_KEY is not set (first seen 2026-08-18)

- [e1c3e6f89daf] `editor`: LLM call failed for 49334409: ANTHROPIC_API_KEY is not set (first seen 2026-08-18)

- [2fe47ea0f3df] `editor`: LLM call failed for 49334991: ANTHROPIC_API_KEY is not set (first seen 2026-08-18)

- [f038065233f2] `editor`: LLM call failed for 49337392: ANTHROPIC_API_KEY is not set (first seen 2026-08-18)

- [799d9580de7e] `editor`: LLM call failed for 49338285: ANTHROPIC_API_KEY is not set (first seen 2026-08-18)

- [2921861d8f09] `editor`: LLM call failed for 49337602: ANTHROPIC_API_KEY is not set (first seen 2026-08-18)

- [50c9ea1c6f9c] `editor`: LLM call failed for 49338328: ANTHROPIC_API_KEY is not set (first seen 2026-08-18)

- [51bb7f0c70bd] `editor`: LLM call failed for 49338459: ANTHROPIC_API_KEY is not set (first seen 2026-08-18)

- [4fc6b71dad0e] `editor`: LLM call failed for 49344654: ANTHROPIC_API_KEY is not set (first seen 2026-08-18)

- [48c869bd6ab9] `editor`: LLM call failed for 49342530: ANTHROPIC_API_KEY is not set (first seen 2026-08-18)

- [8eac5b896252] `editor`: LLM call failed for 49343559: ANTHROPIC_API_KEY is not set (first seen 2026-08-18)

- [2cc2100800db] `editor`: LLM call failed for 49344811: ANTHROPIC_API_KEY is not set (first seen 2026-08-18)

- [2af093e42bc5] `editor`: LLM call failed for 49332495: ANTHROPIC_API_KEY is not set (first seen 2026-08-18)

- [08481b6d4b20] `editor`: LLM call failed for 49345843: ANTHROPIC_API_KEY is not set (first seen 2026-08-18)

- [1139da9fe858] `editor`: LLM call failed for 49272631: ANTHROPIC_API_KEY is not set (first seen 2026-08-18)

- [da879c90f848] `editor`: LLM call failed for 49348751: ANTHROPIC_API_KEY is not set (first seen 2026-08-18)

- [8f001f89610e] `editor`: LLM call failed for 49342719: ANTHROPIC_API_KEY is not set (first seen 2026-08-18)

- [849d52db03f4] `editor`: LLM call failed for 49334960: ANTHROPIC_API_KEY is not set (first seen 2026-08-18)

- [54f15cd793cb] `editor`: LLM call failed for 49345220: ANTHROPIC_API_KEY is not set (first seen 2026-08-18)

- [2c56cd9f4383] `editor`: LLM call failed for 49334209: ANTHROPIC_API_KEY is not set (first seen 2026-08-18)

- [71911fc8f3ef] `editor`: LLM call failed for 49351324: ANTHROPIC_API_KEY is not set (first seen 2026-08-18)

- [c51956f9ef24] `editor`: LLM call failed for 49344825: ANTHROPIC_API_KEY is not set (first seen 2026-08-18)

- [f6520bc1b618] `editor`: LLM call failed for 49345263: ANTHROPIC_API_KEY is not set (first seen 2026-08-18)

- [07f2a9dc54cc] `extractor`: bot-blocked (403): https://asmedigitalcollection.asme.org/sustainablebuildings/article/7/2/024501/1233035/Data-Center-Waste-Heat-as-an-Emerging-Urban (first seen 2026-08-18)

- [0b21159f04f0] `editor`: LLM call failed for 49325159: ANTHROPIC_API_KEY is not set (first seen 2026-08-17)

- [1fad23faf3b0] `editor`: LLM call failed for 49320984: ANTHROPIC_API_KEY is not set (first seen 2026-08-17)

- [4c775399e3b3] `editor`: LLM call failed for 49326156: ANTHROPIC_API_KEY is not set (first seen 2026-08-17)

- [98c9673c4c6a] `editor`: LLM call failed for 49323381: ANTHROPIC_API_KEY is not set (first seen 2026-08-17)

- [be1ac82b2514] `editor`: LLM call failed for 49332981: ANTHROPIC_API_KEY is not set (first seen 2026-08-17)

- [7b991d1864a2] `editor`: LLM call failed for 49325061: ANTHROPIC_API_KEY is not set (first seen 2026-08-17)

- [14c1d90a207f] `editor`: LLM call failed for 49290545: ANTHROPIC_API_KEY is not set (first seen 2026-08-17)

- [bd38545c0dfa] `editor`: LLM call failed for 49324087: ANTHROPIC_API_KEY is not set (first seen 2026-08-17)

- [eef9f5f5d944] `editor`: LLM call failed for 49324985: ANTHROPIC_API_KEY is not set (first seen 2026-08-17)

- [6a5c8c93237c] `editor`: LLM call failed for 49331222: ANTHROPIC_API_KEY is not set (first seen 2026-08-17)

- [122d3d602fe0] `editor`: LLM call failed for 49326816: ANTHROPIC_API_KEY is not set (first seen 2026-08-17)

- [677180f3e3a1] `editor`: LLM call failed for 49325789: ANTHROPIC_API_KEY is not set (first seen 2026-08-17)

- [9fa7575f997f] `editor`: LLM call failed for 49334544: ANTHROPIC_API_KEY is not set (first seen 2026-08-17)

- [6674d3bec201] `editor`: LLM call failed for 49331033: ANTHROPIC_API_KEY is not set (first seen 2026-08-17)

- [e5535ecab9d7] `editor`: LLM call failed for 49336573: ANTHROPIC_API_KEY is not set (first seen 2026-08-17)

- [e8a28d7b53c4] `editor`: LLM call failed for 49331423: ANTHROPIC_API_KEY is not set (first seen 2026-08-17)

- [5234de40df94] `editor`: LLM call failed for 49331220: ANTHROPIC_API_KEY is not set (first seen 2026-08-17)

- [e49ad64035dd] `editor`: LLM call failed for 49270194: ANTHROPIC_API_KEY is not set (first seen 2026-08-17)

- [4159565c13c3] `editor`: LLM call failed for 49329575: ANTHROPIC_API_KEY is not set (first seen 2026-08-17)

- [14b58bfc5602] `editor`: LLM call failed for 49330781: ANTHROPIC_API_KEY is not set (first seen 2026-08-17)

- [5a68a38a9b23] `extractor`: bot-blocked (403): https://www.ischool.berkeley.edu/sites/default/files/vinton_report_5.pdf (first seen 2026-08-17)

- [a6509682aff0] `extractor`: HTTP 401 for https://www.reuters.com/business/nvidia-scales-back-250-billion-openai-data-center-guarantee-wsj-reports-2026-08-14/ (first seen 2026-08-17)

- [1cd8d7d9b6f5] `extractor`: bot-block page detected: https://www.githubstatus.com/incidents/zkxwbgr0cnmx (first seen 2026-08-17)

- [1cf1a7534b04] `editor`: LLM call failed for 49246366: ANTHROPIC_API_KEY is not set (first seen 2026-08-16)

- [a713bc74ba24] `editor`: LLM call failed for 49310926: ANTHROPIC_API_KEY is not set (first seen 2026-08-16)

- [18e763b6fea0] `editor`: LLM call failed for 49317760: ANTHROPIC_API_KEY is not set (first seen 2026-08-16)

- [333b898a8d42] `editor`: LLM call failed for 49310682: ANTHROPIC_API_KEY is not set (first seen 2026-08-16)

- [9222a914275b] `editor`: LLM call failed for 49314403: ANTHROPIC_API_KEY is not set (first seen 2026-08-16)

- [62318c4bf0dc] `editor`: LLM call failed for 49314902: ANTHROPIC_API_KEY is not set (first seen 2026-08-16)

- [13047e2051a2] `editor`: LLM call failed for 49313428: ANTHROPIC_API_KEY is not set (first seen 2026-08-16)

- [e4e92c3674a6] `editor`: LLM call failed for 49314235: ANTHROPIC_API_KEY is not set (first seen 2026-08-16)

- [83187dfa5064] `editor`: LLM call failed for 49243061: ANTHROPIC_API_KEY is not set (first seen 2026-08-16)

- [c7d6c85e9ec7] `editor`: LLM call failed for 49268580: ANTHROPIC_API_KEY is not set (first seen 2026-08-16)

- [f3ee25bec585] `editor`: LLM call failed for 49319633: ANTHROPIC_API_KEY is not set (first seen 2026-08-16)

- [ea2cf55892ad] `editor`: LLM call failed for 49320611: ANTHROPIC_API_KEY is not set (first seen 2026-08-16)

- [6e43c98372f2] `editor`: LLM call failed for 49321717: ANTHROPIC_API_KEY is not set (first seen 2026-08-16)

- [83248d2480ed] `editor`: LLM call failed for 49322695: ANTHROPIC_API_KEY is not set (first seen 2026-08-16)

- [56df4d6014a0] `editor`: LLM call failed for 49319556: ANTHROPIC_API_KEY is not set (first seen 2026-08-16)

- [20058bfc9310] `extractor`: bot-blocked (403): https://scholar.google.com/scholar?q=%22kidney+disappointment%22 (first seen 2026-08-16)

- [32d9c891de57] `extractor`: bot-block page detected: https://news.ycombinator.com/item?id=49322107 (first seen 2026-08-16)

- [deb4d1435243] `editor`: LLM call failed for 49299746: ANTHROPIC_API_KEY is not set (first seen 2026-08-15)

- [c8699f404105] `editor`: LLM call failed for 49299081: ANTHROPIC_API_KEY is not set (first seen 2026-08-15)

- [81de7c759689] `editor`: LLM call failed for 49300568: ANTHROPIC_API_KEY is not set (first seen 2026-08-15)

- [eebc34eeb6f6] `editor`: LLM call failed for 49300800: ANTHROPIC_API_KEY is not set (first seen 2026-08-15)

- [3d27df07bf62] `editor`: LLM call failed for 49300759: ANTHROPIC_API_KEY is not set (first seen 2026-08-15)

- [6f54ac51692c] `editor`: LLM call failed for 49304447: ANTHROPIC_API_KEY is not set (first seen 2026-08-15)

- [5285f352a44c] `editor`: LLM call failed for 49306577: ANTHROPIC_API_KEY is not set (first seen 2026-08-15)

- [486effede269] `editor`: LLM call failed for 49307592: ANTHROPIC_API_KEY is not set (first seen 2026-08-15)

- [d23524b84d2c] `editor`: LLM call failed for 49309451: ANTHROPIC_API_KEY is not set (first seen 2026-08-15)

- [cb853daa3ed9] `editor`: LLM call failed for 49298035: ANTHROPIC_API_KEY is not set (first seen 2026-08-15)

- [6965e244a625] `editor`: LLM call failed for 49312845: ANTHROPIC_API_KEY is not set (first seen 2026-08-15)

- [d33627854c31] `editor`: LLM call failed for 49309549: ANTHROPIC_API_KEY is not set (first seen 2026-08-15)

- [ed00fb84257a] `extractor`: HTTP 401 for https://www.reuters.com/world/frances-top-court-rules-social-media-ban-curtails-freedom-expression-2026-08-14/ (first seen 2026-08-15)

- [93f64f6436a8] `extractor`: bot-blocked (403): https://alz-journals.onlinelibrary.wiley.com/doi/10.1002/dad2.70432 (first seen 2026-08-15)

- [1647cf1706a5] `editor`: LLM call failed for 49279928: ANTHROPIC_API_KEY is not set (first seen 2026-08-14)

- [3131567e56a2] `editor`: LLM call failed for 49286662: ANTHROPIC_API_KEY is not set (first seen 2026-08-14)

- [cd601d4998f6] `editor`: LLM call failed for 49270953: ANTHROPIC_API_KEY is not set (first seen 2026-08-14)

- [11f7ff414581] `editor`: LLM call failed for 49301260: ANTHROPIC_API_KEY is not set (first seen 2026-08-14)

- [ef2b165aed2c] `editor`: LLM call failed for 49276574: ANTHROPIC_API_KEY is not set (first seen 2026-08-14)

- [a7536e77a9a6] `editor`: LLM call failed for 49284774: ANTHROPIC_API_KEY is not set (first seen 2026-08-14)

- [09aefd206123] `editor`: LLM call failed for 49201953: ANTHROPIC_API_KEY is not set (first seen 2026-08-14)

- [4dfba606a153] `editor`: LLM call failed for 49290215: ANTHROPIC_API_KEY is not set (first seen 2026-08-14)

- [b17554a032b9] `editor`: LLM call failed for 49273478: ANTHROPIC_API_KEY is not set (first seen 2026-08-14)

- [c3af514c1d4b] `editor`: LLM call failed for 49280061: ANTHROPIC_API_KEY is not set (first seen 2026-08-14)

- [6dfa04f8c55d] `editor`: LLM call failed for 49285770: ANTHROPIC_API_KEY is not set (first seen 2026-08-14)

- [b20daf298e44] `editor`: LLM call failed for 49289532: ANTHROPIC_API_KEY is not set (first seen 2026-08-14)

- [424e6c0c3b8a] `editor`: LLM call failed for 49289654: ANTHROPIC_API_KEY is not set (first seen 2026-08-14)

- [7a7897174f6d] `editor`: LLM call failed for 49281916: ANTHROPIC_API_KEY is not set (first seen 2026-08-14)

- [e5af4ca8ec0c] `editor`: LLM call failed for 49272832: ANTHROPIC_API_KEY is not set (first seen 2026-08-14)

- [946102309849] `editor`: LLM call failed for 49274600: ANTHROPIC_API_KEY is not set (first seen 2026-08-14)

- [b46f4c5a79f6] `editor`: LLM call failed for 49289465: ANTHROPIC_API_KEY is not set (first seen 2026-08-14)

- [aa3153a9798c] `editor`: LLM call failed for 49285982: ANTHROPIC_API_KEY is not set (first seen 2026-08-14)

- [62d64107a156] `editor`: LLM call failed for 49285418: ANTHROPIC_API_KEY is not set (first seen 2026-08-14)

- [d9165daf7e73] `editor`: LLM call failed for 49293324: ANTHROPIC_API_KEY is not set (first seen 2026-08-14)

- [404d0c64c1f3] `editor`: LLM call failed for 49289512: ANTHROPIC_API_KEY is not set (first seen 2026-08-14)

- [4843cab2e17a] `editor`: LLM call failed for 49290299: ANTHROPIC_API_KEY is not set (first seen 2026-08-14)

- [22a75aa8d662] `editor`: LLM call failed for 49218040: ANTHROPIC_API_KEY is not set (first seen 2026-08-14)

- [271f157bb18d] `editor`: LLM call failed for 49288889: ANTHROPIC_API_KEY is not set (first seen 2026-08-14)

- [564bf492d533] `editor`: LLM call failed for 49291268: ANTHROPIC_API_KEY is not set (first seen 2026-08-14)

- [91dc34efbbb5] `editor`: LLM call failed for 49290166: ANTHROPIC_API_KEY is not set (first seen 2026-08-14)

- [4468c7ea4a1c] `editor`: LLM call failed for 49285327: ANTHROPIC_API_KEY is not set (first seen 2026-08-14)

- [e4929d1c31cb] `editor`: LLM call failed for 49286341: ANTHROPIC_API_KEY is not set (first seen 2026-08-14)

- [2d069909b197] `editor`: LLM call failed for 49285244: ANTHROPIC_API_KEY is not set (first seen 2026-08-14)

- [8ce7b6e9da4a] `editor`: LLM call failed for 49289844: ANTHROPIC_API_KEY is not set (first seen 2026-08-14)

- [b7fdbb90d339] `editor`: LLM call failed for 49289112: ANTHROPIC_API_KEY is not set (first seen 2026-08-14)

- [1d571b3e18fd] `editor`: LLM call failed for 49298910: ANTHROPIC_API_KEY is not set (first seen 2026-08-14)

- [8b64c419654b] `editor`: LLM call failed for 49299222: ANTHROPIC_API_KEY is not set (first seen 2026-08-14)

- [327e4d547c2b] `editor`: LLM call failed for 49249523: ANTHROPIC_API_KEY is not set (first seen 2026-08-14)

- [2a0558530f10] `editor`: LLM call failed for 49299675: ANTHROPIC_API_KEY is not set (first seen 2026-08-14)

- [1a903b284b5d] `editor`: LLM call failed for 49299605: ANTHROPIC_API_KEY is not set (first seen 2026-08-14)

- [3ec69d27fc8e] `editor`: LLM call failed for 49303202: ANTHROPIC_API_KEY is not set (first seen 2026-08-14)

- [4c460e881c82] `editor`: LLM call failed for 49300314: ANTHROPIC_API_KEY is not set (first seen 2026-08-14)

- [4dafc10bf8ad] `editor`: LLM call failed for 49296740: ANTHROPIC_API_KEY is not set (first seen 2026-08-14)

- [641c64ff9f92] `extractor`: bot-blocked (403): https://digitalescapetools.com/2026/08/ublock-origin-stops-chasing-facebook-ads.html (first seen 2026-08-14)

- [65d77c53d6ea] `extractor`: empty body extracted: https://z.ai/blog/glm-5.3 (first seen 2026-08-14)

- [6288704f71b8] `editor`: LLM call failed for 49228458: ANTHROPIC_API_KEY is not set (first seen 2026-08-10)

- [14a1a8f80b40] `editor`: LLM call failed for 49232110: ANTHROPIC_API_KEY is not set (first seen 2026-08-10)

- [2a9a00e0f182] `editor`: LLM call failed for 49234271: ANTHROPIC_API_KEY is not set (first seen 2026-08-10)

- [a2bf7cc0b18e] `editor`: LLM call failed for 49239021: ANTHROPIC_API_KEY is not set (first seen 2026-08-10)

- [b19e17d31db7] `editor`: LLM call failed for 49231809: ANTHROPIC_API_KEY is not set (first seen 2026-08-10)

- [cc374aa3c113] `editor`: LLM call failed for 49232253: ANTHROPIC_API_KEY is not set (first seen 2026-08-10)

- [f80ed4c08747] `editor`: LLM call failed for 49238561: ANTHROPIC_API_KEY is not set (first seen 2026-08-10)

- [955671460ba7] `editor`: LLM call failed for 49245023: ANTHROPIC_API_KEY is not set (first seen 2026-08-10)

- [309158118826] `editor`: LLM call failed for 49242739: ANTHROPIC_API_KEY is not set (first seen 2026-08-10)

- [667359e0cf69] `editor`: LLM call failed for 49239751: ANTHROPIC_API_KEY is not set (first seen 2026-08-10)

- [cdf00cde127c] `editor`: LLM call failed for 49243397: ANTHROPIC_API_KEY is not set (first seen 2026-08-10)

- [0c1e5ca30778] `editor`: LLM call failed for 49249150: ANTHROPIC_API_KEY is not set (first seen 2026-08-10)

- [77c851ff7ee3] `editor`: LLM call failed for 49242653: ANTHROPIC_API_KEY is not set (first seen 2026-08-10)

- [de0a93873627] `editor`: LLM call failed for 49243880: ANTHROPIC_API_KEY is not set (first seen 2026-08-10)

- [7865006d9378] `editor`: LLM call failed for 49241679: ANTHROPIC_API_KEY is not set (first seen 2026-08-10)

- [e4e1becaff96] `extractor`: bot-block page detected: https://www.theatlantic.com/technology/2026/05/ai-wearable-surveillance-countermeasures/687203/ (first seen 2026-08-10)

- [90bd8ae87157] `extractor`: bot-block page detected: https://news.ycombinator.com/item?id=49233423 (first seen 2026-08-10)

- [d753201849ce] `extractor`: bot-blocked (403): https://www.patreon.com/samaaron/posts/sonic-pi-v5-166001392 (first seen 2026-08-10)

- [faf1a25b5618] `editor`: LLM call failed for 49223845: ANTHROPIC_API_KEY is not set (first seen 2026-08-09)

- [28348112e0f3] `editor`: LLM call failed for 49223079: ANTHROPIC_API_KEY is not set (first seen 2026-08-09)

- [52d845830689] `editor`: LLM call failed for 49221939: ANTHROPIC_API_KEY is not set (first seen 2026-08-09)

- [97f49de32eab] `editor`: LLM call failed for 49226536: ANTHROPIC_API_KEY is not set (first seen 2026-08-09)

- [c1e725670a3f] `editor`: LLM call failed for 49221711: ANTHROPIC_API_KEY is not set (first seen 2026-08-09)

- [8f2ba4068fd6] `editor`: LLM call failed for 49215786: ANTHROPIC_API_KEY is not set (first seen 2026-08-09)

- [d81bb88febc0] `editor`: LLM call failed for 49228166: ANTHROPIC_API_KEY is not set (first seen 2026-08-09)

- [705937b46e07] `editor`: LLM call failed for 49226742: ANTHROPIC_API_KEY is not set (first seen 2026-08-09)

- [f82c3fbaaa23] `editor`: LLM call failed for 49226923: ANTHROPIC_API_KEY is not set (first seen 2026-08-09)

- [19643d6e01b8] `editor`: LLM call failed for 49226636: ANTHROPIC_API_KEY is not set (first seen 2026-08-09)

- [ce85645a7047] `editor`: LLM call failed for 49232221: ANTHROPIC_API_KEY is not set (first seen 2026-08-09)

- [177ea9825ec3] `editor`: LLM call failed for 49232138: ANTHROPIC_API_KEY is not set (first seen 2026-08-09)

- [6151729fa40d] `editor`: LLM call failed for 49234675: ANTHROPIC_API_KEY is not set (first seen 2026-08-09)

- [d712815983f6] `editor`: LLM call failed for 49231154: ANTHROPIC_API_KEY is not set (first seen 2026-08-09)

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

