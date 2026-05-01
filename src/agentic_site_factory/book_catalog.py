from __future__ import annotations

import re
from pathlib import Path

from pydantic import BaseModel

from agentic_site_factory.models import SourceDocument
from agentic_site_factory.text_sanitizer import sanitize_body, sanitize_heading


BOOK_KEYWORDS = {
    "book",
    "books",
    "manuscript",
    "novel",
    "novella",
    "memoir",
    "story",
    "stories",
    "chapter",
    "chapters",
    "prologue",
    "epilogue",
    "reader",
    "readers",
    "fiction",
    "nonfiction",
    "poetry",
    "poems",
    "essay",
    "essays",
}

NON_BOOK_FILENAME_KEYWORDS = {
    "notes",
    "bio",
    "biography",
    "outline",
    "plan",
    "spec",
    "summary",
    "resume",
    "readme",
}


class BookItem(BaseModel):
    id: str
    title: str
    source_name: str
    summary: str
    page_filename: str


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", value.strip().lower())
    slug = slug.strip("-")
    return slug or "book"


def title_from_source_name(source_name: str) -> str:
    stem = Path(source_name).stem
    cleaned = re.sub(r"[_-]+", " ", stem)
    cleaned = re.sub(r"\s+", " ", cleaned).strip()

    if not cleaned:
        return "Untitled Book"

    return sanitize_heading(cleaned.title(), fallback="Untitled Book")


def word_count(text: str) -> int:
    return len(re.findall(r"\b\w+\b", text))


def looks_like_book(document: SourceDocument) -> bool:
    filename = document.name.lower()
    text = document.text.lower()
    words = word_count(document.text)

    if any(keyword in filename for keyword in BOOK_KEYWORDS):
        return True

    if any(keyword in filename for keyword in NON_BOOK_FILENAME_KEYWORDS) and words < 1200:
        return False

    keyword_hits = sum(1 for keyword in BOOK_KEYWORDS if keyword in text)

    if words >= 1200:
        return True

    if words >= 350 and keyword_hits >= 2:
        return True

    if keyword_hits >= 4:
        return True

    return False


def summarize_document(document: SourceDocument, max_words: int = 55) -> str:
    cleaned = sanitize_body(document.text)
    sentences = re.split(r"(?<=[.!?])\s+", cleaned)
    summary_words: list[str] = []

    for sentence in sentences:
        for word in sentence.split():
            summary_words.append(word)
            if len(summary_words) >= max_words:
                return " ".join(summary_words).rstrip(" .,;:") + "..."

        if len(summary_words) >= 28:
            break

    summary = " ".join(summary_words).strip()

    if summary:
        return summary

    return "Summary unavailable from the supplied text."


def build_book_catalog(documents: list[SourceDocument]) -> list[BookItem]:
    books: list[BookItem] = []
    used_ids: set[str] = set()

    for document in documents:
        if not looks_like_book(document):
            continue

        base_id = slugify(Path(document.name).stem)
        book_id = base_id
        counter = 2

        while book_id in used_ids:
            book_id = f"{base_id}-{counter}"
            counter += 1

        used_ids.add(book_id)

        books.append(
            BookItem(
                id=book_id,
                title=title_from_source_name(document.name),
                source_name=document.name,
                summary=summarize_document(document),
                page_filename=f"book-{book_id}.html",
            )
        )

    return books
