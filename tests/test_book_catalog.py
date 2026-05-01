from agentic_site_factory.book_catalog import build_book_catalog, looks_like_book
from agentic_site_factory.models import SourceDocument


def test_looks_like_book_detects_book_filename():
    document = SourceDocument(name="my_novel.txt", text="Short text.")

    assert looks_like_book(document)


def test_looks_like_book_ignores_short_bio_notes():
    document = SourceDocument(name="author_bio_notes.txt", text="Short biographical note.")

    assert not looks_like_book(document)


def test_build_book_catalog_creates_summaries_and_pages():
    document = SourceDocument(
        name="coastal_story_manuscript.txt",
        text=(
            "Chapter One. This book follows a family by the sea. "
            "The story explores memory, reconciliation, and hope."
        ),
    )

    books = build_book_catalog([document])

    assert len(books) == 1
    assert books[0].title == "Coastal Story Manuscript"
    assert books[0].page_filename.startswith("book-")
    assert books[0].summary
