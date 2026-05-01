from __future__ import annotations

import re
from html import unescape


HTML_TAG_NAMES = {
    "a",
    "abbr",
    "article",
    "aside",
    "b",
    "blockquote",
    "br",
    "button",
    "caption",
    "cite",
    "code",
    "dd",
    "del",
    "details",
    "div",
    "dl",
    "dt",
    "em",
    "figcaption",
    "figure",
    "footer",
    "h1",
    "h2",
    "h3",
    "h4",
    "h5",
    "h6",
    "header",
    "hr",
    "i",
    "img",
    "li",
    "main",
    "mark",
    "nav",
    "ol",
    "p",
    "pre",
    "section",
    "small",
    "span",
    "strong",
    "sub",
    "summary",
    "sup",
    "table",
    "tbody",
    "td",
    "th",
    "thead",
    "tr",
    "u",
    "ul",
}

TAG_PATTERN = re.compile(r"</?\s*([A-Za-z][A-Za-z0-9-]*)\b[^<>]*?/?>")
ANGLE_WRAPPED_TEXT_PATTERN = re.compile(r"<\s*([^<>]+?)\s*>")
STRAY_ANGLE_PATTERN = re.compile(r"[<>]")
WHITESPACE_PATTERN = re.compile(r"\s+")


def _known_html_tag(match: re.Match[str]) -> str:
    tag_name = match.group(1).lower()
    if tag_name in HTML_TAG_NAMES:
        return ""
    return match.group(0)


def _is_single_known_html_tag(value: str) -> bool:
    match = TAG_PATTERN.fullmatch(value.strip())
    return bool(match and match.group(1).lower() in HTML_TAG_NAMES)


def sanitize_visible_text(value: str, fallback: str = "") -> str:
    cleaned = unescape(value or "").strip()

    if _is_single_known_html_tag(cleaned):
        return fallback

    cleaned = TAG_PATTERN.sub(_known_html_tag, cleaned)
    cleaned = ANGLE_WRAPPED_TEXT_PATTERN.sub(r"\1", cleaned)
    cleaned = STRAY_ANGLE_PATTERN.sub("", cleaned)
    cleaned = WHITESPACE_PATTERN.sub(" ", cleaned).strip()

    return cleaned or fallback


def sanitize_heading(value: str, fallback: str = "Section") -> str:
    return sanitize_visible_text(value, fallback=fallback)


def sanitize_body(value: str, fallback: str = "") -> str:
    return sanitize_visible_text(value, fallback=fallback)
