"""Feed parsing and loading tests."""

from __future__ import annotations

from pathlib import Path

import pytest

from newsmemeai_youtube.feeds import (
    FeedError,
    Headline,
    clean_text,
    collect_headlines,
    fetch_feed,
    parse_feed,
)

RSS = """<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
  <channel>
    <title>Example News</title>
    <item>
      <title>City opens a new park &amp; plaza</title>
      <link>https://example.com/park</link>
      <pubDate>Mon, 16 Nov 2026 09:00:00 GMT</pubDate>
      <description><![CDATA[<p>Council says <b>yes</b>.</p>]]></description>
    </item>
    <item>
      <title>City opens a new park &amp; plaza</title>
      <link>https://example.com/duplicate</link>
    </item>
    <item>
      <title></title>
      <link>https://example.com/empty</link>
    </item>
  </channel>
</rss>
"""

ATOM = """<?xml version="1.0" encoding="utf-8"?>
<feed xmlns="http://www.w3.org/2005/Atom">
  <title>Atom Example</title>
  <entry>
    <title>AI learns to tell jokes</title>
    <link rel="self" href="https://example.com/feed"/>
    <link rel="alternate" href="https://example.com/jokes"/>
    <published>2026-11-16T09:00:00Z</published>
    <summary type="html">&lt;p&gt;A small model &amp;amp; a big punchline.&lt;/p&gt;</summary>
  </entry>
</feed>
"""


def test_parse_rss() -> None:
    headlines = parse_feed(RSS, source="rss")
    assert headlines == [
        Headline(
            title="City opens a new park & plaza",
            link="https://example.com/park",
            source="rss",
            published="Mon, 16 Nov 2026 09:00:00 GMT",
            summary="Council says yes.",
        )
    ]


def test_parse_atom() -> None:
    headlines = parse_feed(ATOM, source="atom")
    assert len(headlines) == 1
    headline = headlines[0]
    assert headline.title == "AI learns to tell jokes"
    assert headline.link == "https://example.com/jokes"
    assert headline.published == "2026-11-16T09:00:00Z"
    assert headline.summary == "A small model & a big punchline."


def test_clean_text() -> None:
    assert clean_text(None) == ""
    assert clean_text("  <p>Hello&nbsp; <b>world</b> </p> ") == "Hello world"


def test_parse_invalid_xml() -> None:
    with pytest.raises(FeedError, match="invalid XML"):
        parse_feed("<rss><channel>", source="broken")


def test_parse_unsupported_document() -> None:
    with pytest.raises(FeedError, match="expected an RSS or Atom feed"):
        parse_feed("<html></html>", source="page")


def test_fetch_local_file(tmp_path: Path) -> None:
    feed = tmp_path / "feed.xml"
    feed.write_text(RSS, encoding="utf-8")
    assert "Example News" in fetch_feed(str(feed))


def test_fetch_missing_file(tmp_path: Path) -> None:
    with pytest.raises(FeedError, match="could not read feed"):
        fetch_feed(str(tmp_path / "missing.xml"))


def test_fetch_bad_url() -> None:
    with pytest.raises(FeedError, match="could not fetch feed"):
        fetch_feed("http://127.0.0.1:1/feed.xml", timeout=0.2)


def test_collect_headlines_dedupes_and_limits(tmp_path: Path) -> None:
    first = tmp_path / "one.xml"
    second = tmp_path / "two.xml"
    first.write_text(RSS, encoding="utf-8")
    second.write_text(ATOM, encoding="utf-8")

    headlines = collect_headlines([str(first), str(second)], limit_per_feed=1)
    assert [headline.title for headline in headlines] == [
        "City opens a new park & plaza",
        "AI learns to tell jokes",
    ]


def test_collect_headlines_rejects_zero_limit() -> None:
    with pytest.raises(ValueError, match="at least 1"):
        collect_headlines(["unused"], limit_per_feed=0)


def test_bundled_fixture_parses() -> None:
    fixture = Path(__file__).parent / "fixtures" / "news.xml"
    headlines = parse_feed(fetch_feed(str(fixture)), source=str(fixture))
    assert [headline.title for headline in headlines] == [
        "Scientists teach robots to smell pizza",
        "City opens a new park & plaza",
        "Moon gets a new parking lot",
    ]
