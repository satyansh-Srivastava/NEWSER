"""Editor Agent -- LLM-synthesizes each successfully-extracted article into
a strict What/Why/Who brief, retrying once if the word count lands outside
config.brief_word_range, and safety-net-truncating (with a logged flag) if
it's still out of range after the retry."""
from __future__ import annotations

import logging
from pathlib import Path

from agents.config import Config
from agents.issue_log import record_issue
from agents.llm_client import ClaudeLLMClient, LLMClient
from agents.models import Brief, RawArticle, dump_json, load_json

logger = logging.getLogger(__name__)

SYSTEM_PROMPT_TEMPLATE = (
    "You are a business news editor. Summarize the given article strictly "
    "into three labeled sections, each on its own line(s), in this exact "
    "order: 'What:', 'Why:', 'Who:'. The combined word count across all "
    "three sections must be between {min_words} and {max_words} words. "
    "Do not include any text outside those three labeled sections.{extra}"
)


def _parse_brief_sections(text: str) -> tuple[str, str, str]:
    sections = {"what": "", "why": "", "who": ""}
    current = None
    for line in text.splitlines():
        stripped = line.strip()
        lowered = stripped.lower()
        if lowered.startswith("what:"):
            current = "what"
            stripped = stripped[len("what:"):].strip()
        elif lowered.startswith("why:"):
            current = "why"
            stripped = stripped[len("why:"):].strip()
        elif lowered.startswith("who:"):
            current = "who"
            stripped = stripped[len("who:"):].strip()
        if current and stripped:
            sections[current] = (sections[current] + " " + stripped).strip()
    return sections["what"], sections["why"], sections["who"]


def _truncate_to_range(what: str, why: str, who: str, max_words: int) -> tuple[str, str, str]:
    sections = {"what": what.split(), "why": why.split(), "who": who.split()}
    overflow = sum(len(words) for words in sections.values()) - max_words
    while overflow > 0:
        longest_key = max(sections, key=lambda k: len(sections[k]))
        if len(sections[longest_key]) <= 5:
            break
        sections[longest_key].pop()
        overflow -= 1
    return " ".join(sections["what"]), " ".join(sections["why"]), " ".join(sections["who"])


def synthesize_one(article: RawArticle, word_range: tuple[int, int], llm: LLMClient) -> Brief | None:
    min_words, max_words = word_range
    extra = ""

    for attempt in range(2):  # spec: reject/retry once if out of range
        system_prompt = SYSTEM_PROMPT_TEMPLATE.format(min_words=min_words, max_words=max_words, extra=extra)
        try:
            raw = llm.complete(system_prompt, f"Title: {article.title}\n\n{article.body_text[:6000]}")
        except Exception as exc:
            record_issue("editor", f"LLM call failed for {article.id}: {exc}", item_id=article.id)
            return None

        what, why, who = _parse_brief_sections(raw)
        word_count = len((what + " " + why + " " + who).split())
        well_formed = bool(what and why and who)

        if well_formed and min_words <= word_count <= max_words:
            return Brief(
                id=article.id, title=article.title, what=what, why=why, who=who,
                source_url=article.url, word_count=word_count,
            )

        if attempt == 0:
            record_issue(
                "editor",
                f"brief malformed or out of word range ({word_count}) for {article.id}, retrying",
                item_id=article.id,
            )
            extra = " Be more concise and precise; strictly obey the word range this time."
            continue

        if not well_formed:
            record_issue("editor", f"brief still missing a required section for {article.id}, dropping", item_id=article.id)
            return None

        record_issue(
            "editor",
            f"brief still out of word range ({word_count}) after retry for {article.id}; truncating and publishing with flag",
            item_id=article.id,
        )
        what, why, who = _truncate_to_range(what, why, who, max_words)
        word_count = len((what + " " + why + " " + who).split())
        return Brief(
            id=article.id, title=article.title, what=what, why=why, who=who,
            source_url=article.url, word_count=word_count,
        )

    return None  # unreachable, satisfies type checkers


def run(
    raw_articles: list[RawArticle],
    config: Config,
    run_dir: Path,
    *,
    llm: LLMClient | None = None,
) -> list[Brief]:
    out_path = run_dir / "briefs.json"
    if out_path.exists():
        raw = load_json(out_path)
        return [Brief(**item) for item in raw]

    llm = llm or ClaudeLLMClient()
    successful = [a for a in raw_articles if a.extraction_status == "success"]

    briefs: list[Brief] = []
    for article in successful:
        brief = synthesize_one(article, config.brief_word_range, llm)
        if brief is not None:
            briefs.append(brief)

    run_dir.mkdir(parents=True, exist_ok=True)
    dump_json(out_path, briefs)
    return briefs
