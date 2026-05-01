from agentic_site_factory.models import GeneratedSection, SiteSpec, SourceDocument
from agentic_site_factory.site_builder import build_html, section_filename


def test_section_filename_creates_real_page_filename():
    section = GeneratedSection(name="books", heading="Books", body="Body")

    assert section_filename(section) == "books.html"


def test_build_html_creates_index_and_section_pages():
    spec = SiteSpec(author_name="Demo Author")
    sections = [
        GeneratedSection(name="bio", heading="About", body="Author biography."),
        GeneratedSection(name="books", heading="Books", body="Book list."),
    ]

    site = build_html(spec, sections)

    assert "index.html" in site.pages
    assert "bio.html" in site.pages
    assert "books.html" in site.pages
    assert 'href="bio.html"' in site.pages["index.html"]
    assert 'href="books.html"' in site.pages["index.html"]
    assert 'href="index.html"' in site.pages["books.html"]


def test_books_page_lists_book_uploads_and_links_to_book_pages():
    spec = SiteSpec(author_name="Demo Author")
    sections = [GeneratedSection(name="books", heading="Books", body="Book list.")]
    documents = [
        SourceDocument(
            name="coastal_story_manuscript.txt",
            text="Chapter One. This book tells a story about coastal memory and hope.",
        )
    ]

    site = build_html(spec, sections, documents=documents)

    assert "books.html" in site.pages
    assert "book-coastal-story-manuscript.html" in site.pages
    assert 'href="book-coastal-story-manuscript.html"' in site.pages["books.html"]
    assert "Add Coastal Story Manuscript to Cart" in site.pages["book-coastal-story-manuscript.html"]


def test_cart_script_uses_local_storage():
    spec = SiteSpec(author_name="Demo Author")
    sections = [GeneratedSection(name="books", heading="Books", body="Book list.")]
    documents = [
        SourceDocument(
            name="coastal_story_manuscript.txt",
            text="Chapter One. This book tells a story about coastal memory and hope.",
        )
    ]

    site = build_html(spec, sections, documents=documents)

    assert "localStorage.getItem" in site.pages["book-coastal-story-manuscript.html"]
    assert "localStorage.setItem" in site.pages["book-coastal-story-manuscript.html"]
    assert "agenticSiteFactoryCart" in site.pages["book-coastal-story-manuscript.html"]
