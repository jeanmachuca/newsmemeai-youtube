"""Dependency-free RSS and Atom ingestion."""

from __future__ import annotations

import html
import re
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET
from collections.abc import Iterable
from dataclasses import dataclass
from pathlib import Path

USER_AGENT = "newsmemeai-youtube/0.1 (+https://github.com/jeanmachuca/newsmemeai-youtube)"
DEFAULT_TIMEOUT = 10.0

_TAG_RE = re.compile(r"<[^>]+>")
_WHITESPACE_RE = re.compile(r"\s+")
_PUNCTUATION_SPACE_RE = re.compile(r"\s+([,.;:!?])")


class FeedError(RuntimeError):
    """Raised when a feed cannot be fetched or parsed."""


@dataclass(frozen=True, slots=True)
class Headline:
    """A single item from an RSS or Atom feed."""

    title: str
    link: str = ""
    source: str = ""
    published: str = ""
    summary: str = ""


def clean_text(value: str | None) -> str:
    """Strip HTML tags and entities, then collapse whitespace."""

    if not value:
        return ""
    without_tags = _TAG_RE.sub(" ", value)
    cleaned = _WHITESPACE_RE.sub(" ", html.unescape(without_tags)).strip()
    return _PUNCTUATION_SPACE_RE.sub(r"\1", cleaned)


def _local_name(tag: object) -> str:
    if not isinstance(tag, str):
        return ""
    return tag.rsplit("}", 1)[-1]


def _first_text(element: ET.Element, names: tuple[str, ...]) -> str:
    for child in element:
        if _local_name(child.tag) in names:
            return clean_text("".join(child.itertext()))
    return ""


def _atom_link(element: ET.Element) -> str:
    fallback = ""
    for child in element:
        if _local_name(child.tag) != "link":
            continue
        href = child.get("href", "").strip()
        if not href:
            continue
        if child.get("rel", "alternate") == "alternate":
            return href
        fallback = fallback or href
    return fallback


def _dedupe(headlines: Iterable[Headline]) -> list[Headline]:
    seen: set[str] = set()
    unique: list[Headline] = []
    for headline in headlines:
        key = headline.title.casefold()
        if key in seen:
            continue
        seen.add(key)
        unique.append(headline)
    return unique


def parse_feed(xml_text: str, *, source: str = "feed") -> list[Headline]:
    """Parse an RSS 2.0 or Atom document into headlines."""

    try:
        root = ET.fromstring(xml_text)
    except ET.ParseError as exc:
        raise FeedError(f"{source}: invalid XML ({exc})") from exc

    kind = _local_name(root.tag)
    if kind == "rss":
        items = [element for element in root.iter() if _local_name(element.tag) == "item"]
        headlines = [
            Headline(
                title=_first_text(item, ("title",)),
                link=_first_text(item, ("link",)),
                source=source,
                published=_first_text(item, ("pubDate", "date")),
                summary=_first_text(item, ("description", "summary", "encoded")),
            )
            for item in items
        ]
    elif kind == "feed":
        entries = [element for element in root.iter() if _local_name(element.tag) == "entry"]
        headlines = [
            Headline(
                title=_first_text(entry, ("title",)),
                link=_atom_link(entry),
                source=source,
                published=_first_text(entry, ("published", "updated")),
                summary=_first_text(entry, ("summary", "content")),
            )
            for entry in entries
        ]
    else:
        raise FeedError(f"{source}: expected an RSS or Atom feed, got <{kind or 'unknown'}>")

    return _dedupe(headline for headline in headlines if headline.title)


def fetch_feed(source: str, *, timeout: float = DEFAULT_TIMEOUT) -> str:
    """Load a feed from an HTTP(S) URL or a local file path."""

    if source.startswith(("http://", "https://")):
        request = urllib.request.Request(source, headers={"User-Agent": USER_AGENT})
        try:
            with urllib.request.urlopen(request, timeout=timeout) as response:
                raw = response.read()
        except (urllib.error.URLError, OSError) as exc:
            raise FeedError(f"{source}: could not fetch feed ({exc})") from exc
        if not isinstance(raw, bytes):
            raise FeedError(f"{source}: feed response did not contain bytes")
        return raw.decode("utf-8", errors="replace")

    path = Path(source).expanduser()
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except OSError as exc:
        raise FeedError(f"{source}: could not read feed ({exc})") from exc


def collect_headlines(
    sources: Iterable[str],
    *,
    limit_per_feed: int = 5,
    timeout: float = DEFAULT_TIMEOUT,
) -> list[Headline]:
    """Fetch several feeds and return a deduplicated list of headlines."""

    if limit_per_feed < 1:
        raise ValueError("limit_per_feed must be at least 1")

    collected: list[Headline] = []
    for source in sources:
        headlines = parse_feed(fetch_feed(source, timeout=timeout), source=source)
        collected.extend(headlines[:limit_per_feed])
    return _dedupe(collected)
