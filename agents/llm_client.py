"""Pluggable LLM client used by the Editor and Classifier agents.

Kept as a small Protocol so it's trivially mockable in tests (no real API
calls, no cost) while defaulting to the Claude API in production. The
`anthropic` package is imported lazily so it's only a hard dependency when
ClaudeLLMClient is actually instantiated.
"""
from __future__ import annotations

import os
from typing import Protocol


class LLMClient(Protocol):
    def complete(self, system: str, user: str) -> str: ...


class ClaudeLLMClient:
    def __init__(self, model: str = "claude-sonnet-5", api_key: str | None = None):
        self.model = model
        self.api_key = api_key or os.environ.get("ANTHROPIC_API_KEY")

    def complete(self, system: str, user: str) -> str:
        if not self.api_key:
            raise RuntimeError("ANTHROPIC_API_KEY is not set")

        import anthropic

        client = anthropic.Anthropic(api_key=self.api_key)
        response = client.messages.create(
            model=self.model,
            max_tokens=700,
            system=system,
            messages=[{"role": "user", "content": user}],
        )
        return "".join(block.text for block in response.content if block.type == "text")
