"""Pytest mapping of the Extractor Agent's Gherkin acceptance criteria in
CLAUDE.md section 3.3."""
from __future__ import annotations

from agents import extractor
from agents.models import QualifiedPost
from tests.conftest import FakeResponse, fake_session


def make_post(url="http://example.com/article") -> QualifiedPost:
    return QualifiedPost(
        id="1", source="hackernews", title="t", url=url, score=250,
        comments=10, subreddit=None, qualified_at="now",
    )


# Scenario: Successful extraction
def test_extract_one_success_populates_body_and_status():
    html = "<html><body><nav>skip</nav><p>Hello world, this is the article.</p></body></html>"
    session = fake_session(lambda *a, **kw: FakeResponse(200, text=html))

    article = extractor.extract_one(make_post(), session=session)

    assert article.extraction_status == "success"
    assert "Hello world" in article.body_text
    assert "<" not in article.body_text  # tags stripped


# Scenario: Bot-blocked source
def test_extract_one_bot_block_page_marked_blocked():
    session = fake_session(lambda *a, **kw: FakeResponse(200, text="Please complete the CAPTCHA to continue"))

    article = extractor.extract_one(make_post(), session=session)

    assert article.extraction_status == "blocked"
    assert article.body_text == ""


def test_extract_one_403_marked_blocked():
    session = fake_session(lambda *a, **kw: FakeResponse(403, text="forbidden"))

    article = extractor.extract_one(make_post(), session=session)

    assert article.extraction_status == "blocked"


def test_extract_one_404_marked_failed():
    session = fake_session(lambda *a, **kw: FakeResponse(404, text="not found"))

    article = extractor.extract_one(make_post(), session=session)

    assert article.extraction_status == "failed"


def test_extract_one_network_error_marked_failed():
    def get(*a, **kw):
        raise ConnectionError("dns failure")

    article = extractor.extract_one(make_post(), session=fake_session(get))

    assert article.extraction_status == "failed"


def test_run_excludes_nothing_from_output_but_flags_status(tmp_path):
    """The pipeline (Editor) is what excludes non-success items downstream;
    the extractor's own output records every attempted item with its
    status, per the raw_articles.json schema."""
    posts = [make_post(url="http://ok.example.com"), make_post(url="http://blocked.example.com")]

    def get(url, headers=None, timeout=None):
        if "blocked" in url:
            return FakeResponse(200, text="Access Denied - CAPTCHA required")
        return FakeResponse(200, text="<p>real article body text here</p>")

    articles = extractor.run(posts, tmp_path / "2026-01-01", session=fake_session(get))

    statuses = {a.extraction_status for a in articles}
    assert statuses == {"success", "blocked"}
