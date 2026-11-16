"""Render storyboard frames and thumbnails as self-contained SVG."""

from __future__ import annotations

import html
from pathlib import Path

VERTICAL_WIDTH = 1080
VERTICAL_HEIGHT = 1920
THUMBNAIL_WIDTH = 1280
THUMBNAIL_HEIGHT = 720
VERTICAL_WRAP = 24
THUMBNAIL_WRAP = 26


def wrap_text(text: str, *, max_chars: int = VERTICAL_WRAP) -> list[str]:
    """Wrap text on word boundaries, preserving explicit line breaks."""

    if max_chars < 1:
        raise ValueError("max_chars must be at least 1")

    lines: list[str] = []
    for paragraph in text.splitlines():
        words: list[str] = []
        for word in paragraph.split():
            while len(word) > max_chars:
                words.append(word[:max_chars])
                word = word[max_chars:]
            if word:
                words.append(word)

        current = ""
        for word in words:
            candidate = f"{current} {word}".strip()
            if len(candidate) <= max_chars:
                current = candidate
                continue
            if current:
                lines.append(current)
            current = word
        if current:
            lines.append(current)
    return lines


def _font_size(lines: list[str], *, vertical: bool) -> int:
    longest = max((len(line) for line in lines), default=0)
    if vertical:
        if longest <= 8:
            return 104
        if longest <= 12:
            return 88
        if longest <= 16:
            return 72
        return 56
    if longest <= 10:
        return 96
    if longest <= 16:
        return 76
    return 60


def _text_block(
    lines: list[str],
    *,
    x: int,
    y: int,
    size: int,
    stroke_width: int,
    fill: str = "#ffffff",
) -> str:
    if not lines:
        return ""
    line_height = round(size * 1.12)
    spans = [
        f'      <tspan x="{x}" dy="{0 if index == 0 else line_height}">{html.escape(line)}</tspan>'
        for index, line in enumerate(lines)
    ]
    return (
        f'    <text x="{x}" y="{y}" font-size="{size}" fill="{fill}" stroke="#000000"\n'
        f'          stroke-width="{stroke_width}" stroke-linejoin="round" '
        f'style="paint-order: stroke fill">\n' + "\n".join(spans) + "\n    </text>"
    )


def _defs(accent: str) -> str:
    return (
        "  <defs>\n"
        '    <linearGradient id="background" x1="0" y1="0" x2="1" y2="1">\n'
        '      <stop offset="0" stop-color="#070a16"/>\n'
        '      <stop offset="0.55" stop-color="#160b33"/>\n'
        '      <stop offset="1" stop-color="#04131f"/>\n'
        "    </linearGradient>\n"
        f'    <radialGradient id="accent" cx="0.5" cy="0.3" r="0.7">\n'
        f'      <stop offset="0" stop-color="{accent}" stop-opacity="0.55"/>\n'
        f'      <stop offset="1" stop-color="{accent}" stop-opacity="0"/>\n'
        "    </radialGradient>\n"
        "  </defs>\n"
    )


def _open_svg(width: int, height: int, *, title: str, description: str) -> str:
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">\n'
        f'  <title id="title">{html.escape(title)}</title>\n'
        f'  <desc id="desc">{html.escape(description)}</desc>\n'
    )


def render_story_frame(
    *,
    kicker: str,
    title: str,
    footer: str,
    index: int,
    total: int = 3,
    accent: str = "#7c5cff",
) -> str:
    """Render one 1080x1920 vertical storyboard frame."""

    lines = wrap_text(title, max_chars=VERTICAL_WRAP)
    size = _font_size(lines, vertical=True)
    line_height = round(size * 1.12)
    first_y = VERTICAL_HEIGHT // 2 - max(0, len(lines) - 1) * line_height // 2
    center = VERTICAL_WIDTH // 2

    return (
        _open_svg(
            VERTICAL_WIDTH,
            VERTICAL_HEIGHT,
            title=f"{kicker} — {title}",
            description="NewsMemeAI YouTube storyboard frame.",
        )
        + _defs(accent)
        + f'  <rect width="{VERTICAL_WIDTH}" height="{VERTICAL_HEIGHT}" '
        'fill="url(#background)"/>\n'
        f'  <circle cx="{center}" cy="640" r="620" fill="url(#accent)"/>\n'
        f'  <text x="72" y="150" font-family="\'JetBrains Mono\',\'SFMono-Regular\',monospace" '
        f'font-size="26" fill="{accent}" letter-spacing="4">{html.escape(kicker.upper())}</text>\n'
        f'  <text x="{VERTICAL_WIDTH - 72}" y="150" text-anchor="end" '
        "font-family=\"'JetBrains Mono','SFMono-Regular',monospace\" "
        f'font-size="26" fill="#8b93b5">{index:02d} / {total:02d}</text>\n'
        "  <g font-family=\"'Anton','Impact','Arial Black',sans-serif\" "
        'font-weight="900" text-anchor="middle">\n'
        f"{_text_block(lines, x=center, y=first_y, size=size, stroke_width=14)}\n"
        "  </g>\n"
        f'  <rect x="72" y="{VERTICAL_HEIGHT - 190}" width="{VERTICAL_WIDTH - 144}" '
        f'height="2" fill="{accent}" opacity="0.5"/>\n'
        f'  <text x="{center}" y="{VERTICAL_HEIGHT - 110}" text-anchor="middle" '
        "font-family=\"'JetBrains Mono','SFMono-Regular',monospace\" "
        f'font-size="24" fill="#9aa4c7">{html.escape(footer)}</text>\n'
        "</svg>\n"
    )


def render_thumbnail(
    *,
    title: str,
    footer: str = "NEWSMEMEAI // YOUTUBE",
    accent: str = "#ff3d81",
) -> str:
    """Render a 1280x720 YouTube thumbnail."""

    lines = wrap_text(title, max_chars=THUMBNAIL_WRAP)
    size = _font_size(lines, vertical=False)
    line_height = round(size * 1.12)
    first_y = THUMBNAIL_HEIGHT // 2 - max(0, len(lines) - 1) * line_height // 2
    center = THUMBNAIL_WIDTH // 2

    return (
        _open_svg(
            THUMBNAIL_WIDTH,
            THUMBNAIL_HEIGHT,
            title=f"Thumbnail — {title}",
            description="NewsMemeAI YouTube thumbnail.",
        )
        + _defs(accent)
        + f'  <rect width="{THUMBNAIL_WIDTH}" height="{THUMBNAIL_HEIGHT}" '
        'fill="url(#background)"/>\n'
        f'  <circle cx="{center}" cy="260" r="520" fill="url(#accent)"/>\n'
        f'  <rect x="56" y="54" width="360" height="62" rx="31" fill="{accent}"/>\n'
        f'  <text x="236" y="96" text-anchor="middle" '
        "font-family=\"'JetBrains Mono','SFMono-Regular',monospace\" "
        'font-size="22" font-weight="700" fill="#080b18" letter-spacing="3">NEWS MEME</text>\n'
        "  <g font-family=\"'Anton','Impact','Arial Black',sans-serif\" "
        'font-weight="900" text-anchor="middle">\n'
        f"{_text_block(lines, x=center, y=first_y, size=size, stroke_width=12)}\n"
        "  </g>\n"
        f'  <text x="{center}" y="{THUMBNAIL_HEIGHT - 46}" text-anchor="middle" '
        "font-family=\"'JetBrains Mono','SFMono-Regular',monospace\" "
        f'font-size="22" fill="#9aa4c7">{html.escape(footer)}</text>\n'
        "</svg>\n"
    )


def write_svg(path: str | Path, content: str) -> Path:
    """Write an SVG document, creating parent directories as needed."""

    destination = Path(path).expanduser()
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(content, encoding="utf-8")
    return destination
