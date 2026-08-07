"""Pytest mapping of the Publisher Agent's Gherkin acceptance criteria in
CLAUDE.md section 3.6."""
from __future__ import annotations

from agents import publisher
from agents.config import DEFAULT_TAXONOMY
from agents.models import TaggedBrief


def tagged_brief(id="1", tags=None) -> TaggedBrief:
    return TaggedBrief(
        id=id, title=f"Title {id}", what="w", why="w", who="w",
        source_url=f"http://x/{id}", word_count=200, tags=tags or ["Funding"],
    )


# Scenario: Page groups by tag
def test_group_by_tag_orders_sections_by_taxonomy_order():
    b1 = tagged_brief("1", tags=["Funding"])
    b2 = tagged_brief("2", tags=["Use-Case News", "Funding"])

    groups = publisher.group_by_tag([b1, b2], DEFAULT_TAXONOMY)
    tag_order = [tag for tag, _ in groups]

    assert tag_order == sorted(tag_order, key=DEFAULT_TAXONOMY.index)


def test_group_by_tag_brief_appears_under_every_assigned_tag():
    b2 = tagged_brief("2", tags=["Use-Case News", "Funding"])

    groups = publisher.group_by_tag([b2], DEFAULT_TAXONOMY)
    groups_by_tag = dict(groups)

    assert b2 in groups_by_tag["Use-Case News"]
    assert b2 in groups_by_tag["Funding"]


# Scenario: Empty day
def test_write_digest_empty_day_shows_message_and_still_archives(tmp_path):
    out_dir = tmp_path / "docs"

    path = publisher.write_digest([], DEFAULT_TAXONOMY, output_dir=str(out_dir))
    html = path.read_text()

    assert "No qualifying stories today" in html
    archive_files = list((out_dir / "archive").glob("*.html"))
    assert len(archive_files) >= 1  # today's (empty) page is archived, not dropped


def test_write_digest_does_not_clobber_previous_days_archive(tmp_path):
    out_dir = tmp_path / "docs"
    archive_dir = out_dir / "archive"
    archive_dir.mkdir(parents=True)
    (archive_dir / "2020-01-01.html").write_text("<html>yesterday</html>")

    publisher.write_digest([], DEFAULT_TAXONOMY, output_dir=str(out_dir))

    assert (archive_dir / "2020-01-01.html").read_text() == "<html>yesterday</html>"


def test_write_digest_renders_briefs_grouped_by_tag(tmp_path):
    out_dir = tmp_path / "docs"

    path = publisher.write_digest([tagged_brief(tags=["Funding"])], DEFAULT_TAXONOMY, output_dir=str(out_dir))
    html = path.read_text()

    assert "Funding" in html
    assert "Title 1" in html
