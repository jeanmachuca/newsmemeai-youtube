#!/usr/bin/env python3
"""Measure the deterministic build path for the HUD Circuit Delta.

Runs the feed -> script -> package pipeline with ``--no-llm`` semantics and reports
the median wall-clock time. All artifacts are written to a temporary directory and
removed afterwards.
"""

from __future__ import annotations

import argparse
import json
import statistics
import sys
import tempfile
import time
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SRC = REPO_ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from newsmemeai_youtube.feeds import collect_headlines  # noqa: E402
from newsmemeai_youtube.package import build_package, slugify  # noqa: E402
from newsmemeai_youtube.script import template_script  # noqa: E402


def _positive_int(value: str) -> int:
    try:
        parsed = int(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("must be an integer") from exc
    if parsed < 1:
        raise argparse.ArgumentTypeError("must be at least 1")
    return parsed


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="benchmark.py",
        description="Measure the median deterministic package build time.",
    )
    parser.add_argument("--runs", type=_positive_int, default=5, metavar="N")
    parser.add_argument(
        "--feed",
        type=Path,
        default=REPO_ROOT / "tests" / "fixtures" / "news.xml",
        metavar="PATH",
    )
    parser.add_argument("--index", type=_positive_int, default=1, metavar="N")
    parser.add_argument("--json", action="store_true", help="emit JSON (default)")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    feed = args.feed.expanduser()
    if not feed.is_file():
        print(f"benchmark: error: feed not found: {feed}", file=sys.stderr)
        return 2

    headlines = collect_headlines([str(feed)], limit_per_feed=args.index)
    if args.index > len(headlines):
        print(
            f"benchmark: error: --index {args.index} is out of range (found {len(headlines)})",
            file=sys.stderr,
        )
        return 2

    headline = headlines[args.index - 1]
    script = template_script(headline, style="classic")
    samples: list[float] = []

    with tempfile.TemporaryDirectory(prefix="newsmemeai-benchmark-") as temporary:
        root = Path(temporary)
        for run in range(args.runs):
            destination = root / f"run-{run:02d}" / slugify(headline.title)
            started = time.perf_counter()
            build_package(headline, script, destination, style="classic")
            samples.append((time.perf_counter() - started) * 1000.0)

    payload = {
        "runs": args.runs,
        "median_ms": round(statistics.median(samples), 2),
        "min_ms": round(min(samples), 2),
        "max_ms": round(max(samples), 2),
        "samples_ms": [round(sample, 2) for sample in samples],
        "feed": str(feed),
        "index": args.index,
        "style": "classic",
        "mode": "no-llm",
    }
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
