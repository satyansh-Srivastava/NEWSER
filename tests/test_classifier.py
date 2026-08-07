"""Pytest mapping of the Classifier Agent's Gherkin acceptance criteria in
CLAUDE.md section 3.5."""
from __future__ import annotations

from agents import classifier
from agents.config import DEFAULT_TAXONOMY
from agents.models import Brief
from tests.conftest import FakeLLM


def make_brief() -> Brief:
    return Brief(
        id="1", title="A new open model", what="w", why="w", who="w",
        source_url="http://x", word_count=200,
    )


# Scenario: Brief gets tagged
def test_classify_one_assigns_valid_taxonomy_tags():
    llm = FakeLLM(["Funding, Open-Source Models"])

    tagged = classifier.classify_one(make_brief(), DEFAULT_TAXONOMY, llm)

    assert 1 <= len(tagged.tags) <= 3
    assert set(tagged.tags) <= set(DEFAULT_TAXONOMY)
    assert tagged.tags == ["Funding", "Open-Source Models"]


def test_classify_one_caps_at_three_tags():
    llm = FakeLLM(["Funding, Open-Source Models, Policy & Regulation, Use-Case News"])

    tagged = classifier.classify_one(make_brief(), DEFAULT_TAXONOMY, llm)

    assert len(tagged.tags) == 3


# Scenario: Ambiguous brief falls back
def test_classify_one_falls_back_when_no_taxonomy_match():
    llm = FakeLLM(["not a real tag at all"])

    tagged = classifier.classify_one(make_brief(), DEFAULT_TAXONOMY, llm)

    assert tagged.tags == ["Use-Case News"]


def test_classify_one_falls_back_on_llm_failure():
    class ExplodingLLM:
        def complete(self, system, user):
            raise RuntimeError("API down")

    tagged = classifier.classify_one(make_brief(), DEFAULT_TAXONOMY, ExplodingLLM())

    assert tagged.tags == ["Use-Case News"]


def test_parse_tags_is_case_insensitive_and_dedupes():
    tags = classifier.parse_tags("funding, FUNDING, open-source models", DEFAULT_TAXONOMY)

    assert tags == ["Funding", "Open-Source Models"]
