from datetime import datetime, timezone

from newser.harness import Digest, Section
from newser.models import NewsItem
from newser.render import render_html, write_digest


def make_digest() -> Digest:
    item = NewsItem(
        title="Anthropic Ships Claude Update",
        url="https://example.com/story",
        source_key="hackernews",
        source_name="Hacker News",
        published=datetime(2026, 8, 7, 12, 0, tzinfo=timezone.utc),
        summary="A short summary.",
        author="jdoe",
        score=250,
        comments=42,
    )
    section = Section(key="hackernews", name="Hacker News", icon="\U0001F7E0", color="#ff6600", items=[item])
    return Digest(generated_at=datetime(2026, 8, 7, 13, 0, tzinfo=timezone.utc), sections=[section])


def test_render_html_includes_item_content():
    html = render_html(make_digest())
    assert "Anthropic Ships Claude Update" in html
    assert "https://example.com/story" in html
    assert "Hacker News" in html
    assert "250" in html


def test_render_html_handles_empty_digest():
    empty = Digest(generated_at=datetime(2026, 8, 7, 13, 0, tzinfo=timezone.utc), sections=[])
    html = render_html(empty)
    assert "No AI stories were found" in html


def test_write_digest_creates_index_and_archive(tmp_path):
    digest = make_digest()
    output_dir = tmp_path / "docs"

    index_path = write_digest(digest, output_dir=str(output_dir))

    assert index_path.exists()
    assert (output_dir / "archive" / "2026-08-07.html").exists()
    assert (output_dir / "archive" / "index.html").exists()
    assert "2026-08-07" in (output_dir / "archive" / "index.html").read_text()
