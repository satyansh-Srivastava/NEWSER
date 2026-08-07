"""Classifier Agent -- assigns 1-3 tags from the locked taxonomy
(config.yaml) to each brief, falling back to "Use-Case News" when nothing
confidently applies so no brief is ever left untagged."""
from __future__ import annotations

import logging
from pathlib import Path

from agents.config import Config
from agents.issue_log import record_issue
from agents.llm_client import ClaudeLLMClient, LLMClient
from agents.models import Brief, TaggedBrief, dump_json, load_json

logger = logging.getLogger(__name__)

FALLBACK_TAG = "Use-Case News"

SYSTEM_PROMPT_TEMPLATE = (
    "You classify a news brief into 1 to 3 tags chosen strictly from this "
    "list, and only this list: {taxonomy}. Reply with only the chosen "
    "tags, comma-separated, spelled exactly as given, nothing else."
)


def parse_tags(raw: str, taxonomy: list[str]) -> list[str]:
    valid = {t.lower(): t for t in taxonomy}
    tags: list[str] = []
    for candidate in raw.split(","):
        key = candidate.strip().lower()
        if key in valid and valid[key] not in tags:
            tags.append(valid[key])
    return tags[:3]


def classify_one(brief: Brief, taxonomy: list[str], llm: LLMClient) -> TaggedBrief:
    system_prompt = SYSTEM_PROMPT_TEMPLATE.format(taxonomy=", ".join(taxonomy))
    user_prompt = f"{brief.title}\n\nWhat: {brief.what}\nWhy: {brief.why}\nWho: {brief.who}"

    tags: list[str] = []
    try:
        raw = llm.complete(system_prompt, user_prompt)
        tags = parse_tags(raw, taxonomy)
    except Exception as exc:
        record_issue("classifier", f"LLM call failed for {brief.id}: {exc}", item_id=brief.id)

    if not tags:  # covers both a failed LLM call and a non-taxonomy reply
        record_issue("classifier", f"no confident tag for {brief.id}, using fallback", item_id=brief.id)
        tags = [FALLBACK_TAG]

    return TaggedBrief(
        id=brief.id, title=brief.title, what=brief.what, why=brief.why, who=brief.who,
        source_url=brief.source_url, word_count=brief.word_count, tags=tags,
    )


def run(
    briefs: list[Brief],
    config: Config,
    run_dir: Path,
    *,
    llm: LLMClient | None = None,
) -> list[TaggedBrief]:
    out_path = run_dir / "tagged_briefs.json"
    if out_path.exists():
        raw = load_json(out_path)
        return [TaggedBrief(**item) for item in raw]

    llm = llm or ClaudeLLMClient()
    tagged = [classify_one(brief, config.taxonomy, llm) for brief in briefs]

    run_dir.mkdir(parents=True, exist_ok=True)
    dump_json(out_path, tagged)
    return tagged
