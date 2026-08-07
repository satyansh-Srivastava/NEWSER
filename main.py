"""CLI entrypoint: runs the full Glueball pipeline once.

Usage:
    python main.py
    python main.py --output-dir docs
    python main.py --config config.yaml -v
"""
from __future__ import annotations

import argparse
import json
import logging
import sys

from agents import orchestrator
from agents.config import Config


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the Glueball daily AI newsletter pipeline once.")
    parser.add_argument("--config", default=None, help="Path to config.yaml (default: repo root config.yaml)")
    parser.add_argument("--output-dir", default="docs", help="Directory to write index.html + archive/ into")
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable debug logging")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )

    config = Config.load(args.config)
    summary = orchestrator.run(config, output_dir=args.output_dir)
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
