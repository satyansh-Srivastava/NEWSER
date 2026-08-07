from datetime import datetime, timezone

from newser.filters import dedupe, is_ai_related
from newser.models import NewsItem


def make_item(title: str, source_key: str = "src", **kwargs) -> NewsItem:
    return NewsItem(
        title=title,
        url=f"https://example.com/{title}",
        source_key=source_key,
        source_name=source_key,
        published=datetime(2026, 1, 1, tzinfo=timezone.utc),
        **kwargs,
    )


def test_is_ai_related_matches_known_keywords():
    assert is_ai_related("OpenAI releases new GPT model")
    assert is_ai_related("A deep dive into machine learning pipelines")
    assert is_ai_related("Anthropic's Claude gets an update")


def test_is_ai_related_rejects_unrelated_titles():
    assert not is_ai_related("Local bakery wins award for best sourdough")
    assert not is_ai_related("Congress passes new budget bill")


def test_is_ai_related_does_not_false_positive_on_substring():
    # "ai" must not match inside unrelated words like "said" or "certain"
    assert not is_ai_related("She said the plan was certain to fail")


def test_dedupe_drops_repeated_titles_keeping_first():
    items = [
        make_item("OpenAI Ships New Model", source_key="techcrunch_ai"),
        make_item("OpenAI ships new model!", source_key="google_news_ai"),  # dup, diff punctuation/case
        make_item("Completely Different Story", source_key="google_news_ai"),
    ]
    result = dedupe(items)
    assert len(result) == 2
    assert result[0].source_key == "techcrunch_ai"
    assert result[1].title == "Completely Different Story"


def test_dedupe_preserves_order_for_unique_items():
    items = [make_item("First"), make_item("Second"), make_item("Third")]
    result = dedupe(items)
    assert [i.title for i in result] == ["First", "Second", "Third"]
