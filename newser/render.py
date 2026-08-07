"""Renders a Digest into the visual HTML article, plus a browsable archive."""
from __future__ import annotations

import re
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, select_autoescape

from newser import config
from newser.harness import Digest

_TEMPLATES_DIR = Path(__file__).parent / "templates"

_env = Environment(
    loader=FileSystemLoader(str(_TEMPLATES_DIR)),
    autoescape=select_autoescape(["html", "jinja"]),
)


def render_html(digest: Digest) -> str:
    template = _env.get_template("digest.html.jinja")
    date_str = digest.generated_at.strftime("%A, %B %d, %Y")
    generated_at_str = digest.generated_at.strftime("%H:%M UTC")
    return template.render(
        digest=digest,
        date_str=date_str,
        generated_at_str=generated_at_str,
        twitter_enabled=config.ENABLE_TWITTER,
    )


def write_digest(digest: Digest, output_dir: str = config.OUTPUT_DIR) -> Path:
    """Writes the digest to `output_dir/index.html`, archives a dated copy
    under `output_dir/archive/`, and regenerates the archive index."""
    out_dir = Path(output_dir)
    archive_dir = out_dir / "archive"
    archive_dir.mkdir(parents=True, exist_ok=True)

    html = render_html(digest)
    index_path = out_dir / "index.html"
    index_path.write_text(html, encoding="utf-8")

    date_key = digest.generated_at.strftime("%Y-%m-%d")
    archive_path = archive_dir / f"{date_key}.html"
    archive_path.write_text(html, encoding="utf-8")

    _write_archive_index(archive_dir)
    return index_path


def _write_archive_index(archive_dir: Path) -> None:
    date_pattern = re.compile(r"^\d{4}-\d{2}-\d{2}\.html$")
    dated_files = sorted(
        (p for p in archive_dir.glob("*.html") if date_pattern.match(p.name)),
        key=lambda p: p.name,
        reverse=True,
    )

    rows = "\n".join(
        f'    <li><a href="./{p.name}">{p.stem}</a></li>' for p in dated_files
    )
    html = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Newser -- Archive</title>
<style>
  body {{ font-family: -apple-system, Segoe UI, Roboto, sans-serif; max-width: 640px;
          margin: 3rem auto; padding: 0 1rem; color: #16181d; }}
  h1 {{ font-size: 1.4rem; }}
  ul {{ list-style: none; padding: 0; }}
  li {{ margin: .4rem 0; }}
  a {{ color: #6366f1; text-decoration: none; font-weight: 600; }}
  a:hover {{ text-decoration: underline; }}
  .back {{ display: inline-block; margin-bottom: 1.5rem; color: #5b6270; }}
</style>
</head>
<body>
  <a class="back" href="../index.html">&larr; Back to latest digest</a>
  <h1>Newser Archive</h1>
  <ul>
{rows}
  </ul>
</body>
</html>
"""
    (archive_dir / "index.html").write_text(html, encoding="utf-8")
