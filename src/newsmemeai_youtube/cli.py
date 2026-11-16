"""Command-line entry point for NewsMemeAI YouTube."""

from __future__ import annotations

import argparse
import json
import sys
from collections.abc import Sequence
from dataclasses import asdict
from pathlib import Path

from . import __version__
from .feeds import FeedError, Headline, collect_headlines
from .package import PackageError, build_package, slugify
from .script import (
    STYLES,
    ModelError,
    Script,
    ScriptError,
    generate_script,
    template_script,
)
from .validate import validate_package

DEFAULT_FEEDS = (
    "https://feeds.bbci.co.uk/news/rss.xml",
    "https://www.theverge.com/rss/index.xml",
)


def _positive_int(value: str) -> int:
    try:
        parsed = int(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("must be an integer") from exc
    if parsed < 1:
        raise argparse.ArgumentTypeError("must be at least 1")
    return parsed


def _positive_float(value: str) -> float:
    try:
        parsed = float(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("must be a number") from exc
    if parsed <= 0:
        raise argparse.ArgumentTypeError("must be greater than zero")
    return parsed


def _add_feed_options(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--feed",
        action="append",
        dest="feeds",
        metavar="URL_OR_PATH",
        help="RSS/Atom URL or local file; repeat for multiple feeds",
    )
    parser.add_argument(
        "--limit",
        type=_positive_int,
        default=5,
        metavar="N",
        help="headlines per feed (default: 5)",
    )
    parser.add_argument(
        "--timeout",
        type=_positive_float,
        default=10.0,
        metavar="SECONDS",
        help="network timeout (default: 10)",
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="newsmemeai-youtube",
        description="Turn news headlines into review-ready YouTube Shorts packages.",
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    subparsers = parser.add_subparsers(dest="command", required=True)

    headlines = subparsers.add_parser("headlines", help="list the latest headlines")
    _add_feed_options(headlines)
    headlines.add_argument("--json", action="store_true", help="emit JSON")

    build = subparsers.add_parser("build", help="build a Shorts package from one headline")
    _add_feed_options(build)
    build.add_argument(
        "--index",
        type=_positive_int,
        default=1,
        metavar="N",
        help="1-based headline to use (default: 1)",
    )
    build.add_argument(
        "--style",
        choices=STYLES,
        default="classic",
        help="script style (default: classic)",
    )
    build.add_argument(
        "--out",
        metavar="DIR",
        help="package directory (default: out/<headline-slug>)",
    )
    build.add_argument(
        "--no-llm",
        action="store_true",
        help="use the deterministic template even when a model is configured",
    )
    build.add_argument("--json", action="store_true", help="emit the manifest as JSON")

    validate = subparsers.add_parser("validate", help="verify a package and its checksums")
    validate.add_argument("package", metavar="DIR", help="package directory to validate")
    validate.add_argument("--json", action="store_true", help="emit JSON")

    return parser


def _sources(args: argparse.Namespace) -> list[str]:
    return list(args.feeds) if args.feeds else list(DEFAULT_FEEDS)


def _cmd_headlines(args: argparse.Namespace) -> int:
    headlines = collect_headlines(
        _sources(args),
        limit_per_feed=args.limit,
        timeout=args.timeout,
    )
    if args.json:
        payload = [asdict(headline) for headline in headlines]
        print(json.dumps(payload, indent=2, ensure_ascii=False))
        return 0
    if not headlines:
        print("newsmemeai-youtube: no headlines found", file=sys.stderr)
        return 1

    for index, headline in enumerate(headlines, start=1):
        print(f"{index:2}. {headline.title}")
        details = headline.source
        if headline.published:
            details = f"{details} · {headline.published}"
        print(f"    {details}")
    return 0


def _caption_for(args: argparse.Namespace, headline: Headline) -> Script:
    if args.no_llm:
        return template_script(headline, style=args.style)
    return generate_script(headline, style=args.style)


def _cmd_build(args: argparse.Namespace) -> int:
    headlines = collect_headlines(
        _sources(args),
        limit_per_feed=args.limit,
        timeout=args.timeout,
    )
    if not headlines:
        print("newsmemeai-youtube: no headlines found", file=sys.stderr)
        return 1
    if args.index > len(headlines):
        raise ScriptError(f"--index {args.index} is out of range (found {len(headlines)})")

    headline = headlines[args.index - 1]
    script = _caption_for(args, headline)
    destination = Path(args.out).expanduser() if args.out else Path("out") / slugify(headline.title)
    package = build_package(headline, script, destination, style=args.style)

    manifest = json.loads((package / "manifest.json").read_text(encoding="utf-8"))
    if args.json:
        payload = {"package": str(package), "manifest": manifest}
        print(json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=True))
        return 0

    print(f"Wrote package: {package}")
    print(f"Headline: {headline.title}")
    print(f"Hook: {script.hook}")
    print(f"Review required: {package / 'REVIEW.md'}")
    print("Status: draft (nothing was published)")
    return 0


def _cmd_validate(args: argparse.Namespace) -> int:
    result = validate_package(args.package)
    if args.json:
        print(
            json.dumps(
                {
                    "package": str(result.package),
                    "ok": result.ok,
                    "files_checked": result.files_checked,
                    "issues": list(result.issues),
                },
                indent=2,
                ensure_ascii=False,
            )
        )
    elif result.ok:
        print(f"OK: {result.files_checked} files verified in {result.package}")
    else:
        print(f"INVALID: {result.package}", file=sys.stderr)
        for issue in result.issues:
            print(f"  - {issue}", file=sys.stderr)
    return 0 if result.ok else 1


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        if args.command == "headlines":
            return _cmd_headlines(args)
        if args.command == "validate":
            return _cmd_validate(args)
        return _cmd_build(args)
    except (FeedError, ScriptError, ModelError, PackageError, OSError, ValueError) as exc:
        print(f"newsmemeai-youtube: error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
