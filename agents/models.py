"""Shared data contracts (dataclasses) for every stage of the Glueball
pipeline, matching the JSON schemas in CLAUDE.md section 3."""
from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Optional


@dataclass
class QualifiedPost:
    id: str
    source: str  # "hackernews" | "reddit"
    title: str
    url: str
    score: float
    comments: int
    subreddit: Optional[str]
    qualified_at: str  # ISO8601


@dataclass
class RawArticle:
    id: str
    url: str
    title: str
    source: str
    body_text: str
    extraction_status: str  # "success" | "blocked" | "failed"


@dataclass
class Brief:
    id: str
    title: str
    what: str
    why: str
    who: str
    source_url: str
    word_count: int


@dataclass
class TaggedBrief:
    id: str
    title: str
    what: str
    why: str
    who: str
    source_url: str
    word_count: int
    tags: list[str]


def dump_json(path: Path, items: list) -> None:
    path.write_text(json.dumps([asdict(item) for item in items], indent=2))


def load_json(path: Path) -> list[dict]:
    return json.loads(path.read_text())
