from agentic_site_factory.models import GeneratedSection, SiteSpec
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
