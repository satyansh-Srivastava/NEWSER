"""Loads config.yaml -- the only human touchpoint (see CLAUDE.md section 2).
No tunable threshold/taxonomy value should ever be hardcoded in an agent;
it belongs here instead."""
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_CONFIG_PATH = REPO_ROOT / "config.yaml"

DEFAULT_SUBREDDITS = ["artificial", "MachineLearning", "SaaS"]
DEFAULT_TAXONOMY = [
    "Use-Case News",
    "Novel SaaS/Tech",
    "Open-Source Models",
    "Policy & Regulation",
    "Funding",
]


@dataclass
class Config:
    hn_threshold: int = 200
    reddit_ratio: float = 10.0
    subreddits: list[str] = field(default_factory=lambda: list(DEFAULT_SUBREDDITS))
    taxonomy: list[str] = field(default_factory=lambda: list(DEFAULT_TAXONOMY))
    schedule_cron: str = "0 23 * * *"
    brief_word_range: tuple[int, int] = (180, 280)

    @classmethod
    def load(cls, path: Path | str | None = None) -> "Config":
        path = Path(path) if path else DEFAULT_CONFIG_PATH
        if not path.exists():
            return cls()

        raw = yaml.safe_load(path.read_text()) or {}
        defaults = cls()
        word_range = raw.get("brief_word_range", defaults.brief_word_range)
        return cls(
            hn_threshold=raw.get("hn_threshold", defaults.hn_threshold),
            reddit_ratio=raw.get("reddit_ratio", defaults.reddit_ratio),
            subreddits=raw.get("subreddits", defaults.subreddits),
            taxonomy=raw.get("taxonomy", defaults.taxonomy),
            schedule_cron=raw.get("schedule_cron", defaults.schedule_cron),
            brief_word_range=tuple(word_range),
        )
