"""Central configuration for the newser digest agent."""
from __future__ import annotations

import os

# Where the generated HTML digest is written. GitHub Pages serves this
# directory directly when Pages is configured for "/docs" on the default
# branch.
OUTPUT_DIR = os.environ.get("NEWSER_OUTPUT_DIR", "docs")

# A generic User-Agent is required by Reddit's .json endpoints and is
# good etiquette for every other HTTP fetch we do.
USER_AGENT = "newser-digest-agent/0.1 (+https://github.com/satyansh-Srivastava/NEWSER)"

REQUEST_TIMEOUT_SECONDS = 10

# --- Hacker News -----------------------------------------------------------
# The official Firebase API has no topic filter, so we scan the top stories
# and keep only the ones whose titles look AI-related.
HN_TOP_STORIES_URL = "https://hacker-news.firebaseio.com/v0/topstories.json"
HN_ITEM_URL = "https://hacker-news.firebaseio.com/v0/item/{id}.json"
HN_STORIES_TO_SCAN = 120
HN_MAX_ITEMS = 15

# --- Reddit ------------------------------------------------------------------
REDDIT_SUBREDDITS = ["artificial", "MachineLearning"]
REDDIT_LISTING = "hot"   # hot | new | top
REDDIT_LIMIT = 25
REDDIT_MAX_ITEMS_PER_SUB = 10

# --- ArXiv ---------------------------------------------------------------
ARXIV_RSS_URL = "https://export.arxiv.org/rss/cs.AI"
ARXIV_MAX_ITEMS = 15

# --- Generic RSS feeds (already AI-scoped, no keyword filtering needed) ---
RSS_FEEDS = [
    {
        "key": "techcrunch_ai",
        "name": "TechCrunch AI",
        "url": "https://techcrunch.com/category/artificial-intelligence/feed/",
        "max_items": 10,
    },
    {
        "key": "venturebeat_ai",
        "name": "VentureBeat AI",
        "url": "https://venturebeat.com/category/ai/feed/",
        "max_items": 10,
    },
    {
        "key": "google_news_ai",
        "name": "Google News: AI",
        "url": "https://news.google.com/rss/search?q=AI+when:1d&hl=en-US&gl=US&ceid=US:en",
        "max_items": 15,
    },
]

# --- Twitter/X -------------------------------------------------------------
# Requires a paid API tier. Stubbed out and disabled by default; flip this
# on (and implement newser/fetchers/twitter.py) once you have API access.
ENABLE_TWITTER = False

# --- Relevance filtering -----------------------------------------------------
# Used only for sources that aren't already topically scoped (i.e. Hacker
# News top stories, which cover everything).
AI_KEYWORDS = [
    "ai", "a.i.", "artificial intelligence", "machine learning", "ml model",
    "llm", "large language model", "gpt", "chatgpt", "openai", "anthropic",
    "claude", "gemini", "deepmind", "neural network", "deep learning",
    "generative ai", "genai", "transformer", "agentic", "copilot",
    "stable diffusion", "midjourney", "diffusion model", "chatbot",
]

# --- Section display order / styling ---------------------------------------
SECTION_META = {
    "hackernews": {"name": "Hacker News", "icon": "\U0001F7E0", "color": "#ff6600"},
    "reddit_artificial": {"name": "r/artificial", "icon": "\U0001F47D", "color": "#ff4500"},
    "reddit_machinelearning": {"name": "r/MachineLearning", "icon": "\U0001F9E0", "color": "#ff4500"},
    "arxiv": {"name": "arXiv cs.AI", "icon": "\U0001F4C4", "color": "#b31b1b"},
    "techcrunch_ai": {"name": "TechCrunch AI", "icon": "\U0001F4F0", "color": "#0a9d00"},
    "venturebeat_ai": {"name": "VentureBeat AI", "icon": "\U0001F4E1", "color": "#1a73e8"},
    "google_news_ai": {"name": "Google News: AI", "icon": "\U0001F50D", "color": "#4285f4"},
    "twitter": {"name": "Twitter/X", "icon": "\U0001F426", "color": "#000000"},
}
