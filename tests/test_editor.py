"""Pytest mapping of the Editor Agent's Gherkin acceptance criteria in
CLAUDE.md section 3.4."""
from __future__ import annotations

from agents import editor
from agents.models import RawArticle
from tests.conftest import FakeLLM


def make_article() -> RawArticle:
    return RawArticle(
        id="1", url="http://example.com/article", title="Some Title",
        source="hackernews", body_text="a" * 500, extraction_status="success",
    )


def brief_text(what_words: int, why_words: int, who_words: int) -> str:
    return (
        "What: " + ("word " * what_words).strip() + "\n"
        "Why: " + ("word " * why_words).strip() + "\n"
        "Who: " + ("word " * who_words).strip()
    )


# Scenario: Well-formed brief
def test_well_formed_brief_within_word_range():
    llm = FakeLLM([brief_text(70, 70, 70)])  # 210 words total

    brief = editor.synthesize_one(make_article(), (180, 280), llm)

    assert brief is not None
    assert brief.what and brief.why and brief.who
    assert 180 <= brief.word_count <= 280
    assert brief.source_url == "http://example.com/article"


# Scenario: Oversized output retried
def test_oversized_output_is_retried_and_succeeds():
    too_long = brief_text(150, 150, 150)  # 450 words
    ok = brief_text(70, 70, 70)
    llm = FakeLLM([too_long, ok])

    brief = editor.synthesize_one(make_article(), (180, 280), llm)

    assert len(llm.calls) == 2
    assert 180 <= brief.word_count <= 280


def test_still_oversized_after_retry_is_truncated_and_flagged():
    too_long = brief_text(150, 150, 150)
    llm = FakeLLM([too_long, too_long])

    brief = editor.synthesize_one(make_article(), (180, 280), llm)

    assert brief is not None
    assert brief.word_count <= 280
    assert brief.what and brief.why and brief.who


def test_brief_missing_a_section_after_retry_is_dropped():
    malformed = "What: word word\nWhy: word word"  # no Who: section, both attempts
    llm = FakeLLM([malformed, malformed])

    brief = editor.synthesize_one(make_article(), (180, 280), llm)

    assert brief is None


def test_llm_failure_drops_article_without_crashing():
    class ExplodingLLM:
        def complete(self, system, user):
            raise RuntimeError("API down")

    brief = editor.synthesize_one(make_article(), (180, 280), ExplodingLLM())

    assert brief is None


def test_run_only_synthesizes_successfully_extracted_articles(tmp_path):
    articles = [
        make_article(),
        RawArticle(id="2", url="http://x", title="t2", source="reddit", body_text="", extraction_status="blocked"),
    ]
    llm = FakeLLM([brief_text(70, 70, 70)])

    from agents.config import Config
    briefs = editor.run(articles, Config(), tmp_path / "2026-01-01", llm=llm)

    assert len(briefs) == 1
    assert briefs[0].id == "1"
