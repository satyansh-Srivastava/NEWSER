"""CLI entrypoint for the newser digest agent.

Usage:
    python -m newser.main
    python -m newser.main --dry-run
    python -m newser.main --sources hackernews,arxiv
    python -m newser.main --output-dir docs --max-per-source 5
"""
from __future__ import annotations

import argparse
import logging
import sys

from newser import config, harness, render


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Fetch and render the daily AI news digest.")
    parser.add_argument(
        "--output-dir",
        default=config.OUTPUT_DIR,
        help="Directory to write index.html and archive/ into (default: %(default)s)",
    )
    parser.add_argument(
        "--sources",
        default=None,
        help="Comma-separated source keys to run (default: all enabled sources). "
        "See newser/config.py SECTION_META for valid keys.",
    )
    parser.add_argument(
        "--max-per-source",
        type=int,
        default=None,
        help="Cap the number of items rendered per source, after dedupe.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Fetch and print summary stats without writing any HTML.",
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable debug logging.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )

    enabled_sources = set(args.sources.split(",")) if args.sources else None
    digest = harness.build_digest(
        enabled_sources=enabled_sources,
        max_per_source=args.max_per_source,
    )

    if args.dry_run:
        print(f"Fetched {digest.total_items} items across {digest.source_count} sources:")
        for section in digest.sections:
            print(f"  {section.icon} {section.name}: {len(section.items)}")
        return 0

    path = render.write_digest(digest, output_dir=args.output_dir)
    print(f"Wrote digest ({digest.total_items} items, {digest.source_count} sources) to {path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
