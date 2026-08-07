"""Publisher Agent -- renders tagged briefs into a static, light-mode-only,
typography-first HTML digest grouped by taxonomy tag (in taxonomy order),
and writes it (+ a dated archive copy) to docs/. Committing and pushing
docs/ to trigger the GitHub Pages rebuild is handled by the GitHub Actions
workflow, not this module.
"""
from __future__ import annotations

import re
from datetime import datetime, timezone
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, select_autoescape

from agents.config import Config
from agents.models import TaggedBrief

TEMPLATES_DIR = Path(__file__).resolve().parent.parent / "templates"

_env = Environment(
    loader=FileSystemLoader(str(TEMPLATES_DIR)),
    autoescape=select_autoescape(["html", "jinja"]),
)


def group_by_tag(briefs: list[TaggedBrief], taxonomy: list[str]) -> list[tuple[str, list[TaggedBrief]]]:
    """Groups briefs under each tag they carry, in taxonomy order. A brief
    with multiple tags appears once under every matching section."""
    groups: list[tuple[str, list[TaggedBrief]]] = []
    for tag in taxonomy:
        matching = [b for b in briefs if tag in b.tags]
        if matching:
            groups.append((tag, matching))
    return groups


def render_html(briefs: list[TaggedBrief], taxonomy: list[str], generated_at: datetime) -> str:
    template = _env.get_template("digest.html.jinja")
    groups = group_by_tag(briefs, taxonomy)
    return template.render(
        groups=groups,
        total=len(briefs),
        date_str=generated_at.strftime("%A, %B %d, %Y"),
        time_str=generated_at.strftime("%H:%M UTC"),
    )


def write_digest(briefs: list[TaggedBrief], taxonomy: list[str], output_dir: str = "docs") -> Path:
    """Always writes docs/index.html AND a dated docs/archive/YYYY-MM-DD.html
    copy -- including on an empty day -- so a zero-brief day never silently
    erases the archive's continuity (see the 'Empty day' acceptance
    scenario in CLAUDE.md section 3.6)."""
    out_dir = Path(output_dir)
    archive_dir = out_dir / "archive"
    archive_dir.mkdir(parents=True, exist_ok=True)

    generated_at = datetime.now(timezone.utc)
    html = render_html(briefs, taxonomy, generated_at)

    index_path = out_dir / "index.html"
    index_path.write_text(html, encoding="utf-8")

    date_key = generated_at.strftime("%Y-%m-%d")
    (archive_dir / f"{date_key}.html").write_text(html, encoding="utf-8")

    _write_archive_index(archive_dir)
    return index_path


def _write_archive_index(archive_dir: Path) -> None:
    date_pattern = re.compile(r"^\d{4}-\d{2}-\d{2}\.html$")
    dated_files = sorted(
        (p for p in archive_dir.glob("*.html") if date_pattern.match(p.name)),
        key=lambda p: p.name,
        reverse=True,
    )
    rows = "\n".join(f'    <li><a href="./{p.name}">{p.stem}</a></li>' for p in dated_files)
    html = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Glueball -- Archive</title>
<style>
  body {{ font-family: Georgia, 'Times New Roman', serif; max-width: 640px;
          margin: 3rem auto; padding: 0 1rem; color: #111; background: #fff; }}
  h1 {{ font-size: 1.2rem; }}
  ul {{ list-style: none; padding: 0; }}
  li {{ margin: .3rem 0; }}
  a {{ color: #0645ad; text-decoration: none; }}
  a:hover {{ text-decoration: underline; }}
  .back {{ display: inline-block; margin-bottom: 1.2rem; color: #555; font-size: .85rem; }}
</style>
</head>
<body>
  <a class="back" href="../index.html">&larr; Back to latest digest</a>
  <h1>Glueball Archive</h1>
  <ul>
{rows}
  </ul>
</body>
</html>
"""
    (archive_dir / "index.html").write_text(html, encoding="utf-8")


def run(tagged_briefs: list[TaggedBrief], config: Config, output_dir: str = "docs") -> Path:
    return write_digest(tagged_briefs, config.taxonomy, output_dir=output_dir)
