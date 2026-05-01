from pathlib import Path

from agentic_site_factory.models import GeneratedSection, SiteSpec
from agentic_site_factory.site_builder import build_html, clean_heading, save_site


def test_clean_heading_removes_angle_wrappers():
    assert clean_heading("<Books>") == "Books"


def test_clean_heading_uses_fallback_for_html_tag():
    assert clean_heading("<br>") == "Section"


def test_build_html_contains_author_name():
    spec = SiteSpec(author_name="Demo Author")
    sections = [GeneratedSection(name="bio", heading="About", body="Author biography.")]

    site = build_html(spec, sections)

    assert "Demo Author" in site.html
    assert "Author biography." in site.html
    assert site.theme.name


def test_build_html_nav_uses_in_page_scroll_handler():
    spec = SiteSpec(author_name="Demo Author")
    sections = [GeneratedSection(name="books", heading="<Books>", body="Book list.")]

    site = build_html(spec, sections)

    assert "data-target=\"books\"" in site.html
    assert "scrollIntoView" in site.html
    assert "<Books>" not in site.html


def test_build_html_sanitizes_visible_body_text():
    spec = SiteSpec(author_name="Demo Author")
    sections = [
        GeneratedSection(
            name="books",
            heading="Books",
            body="Read <Featured Books> and <strong>new stories</strong>.",
        )
    ]

    site = build_html(spec, sections)

    assert "Read Featured Books and new stories." in site.html
    assert "&lt;Featured Books&gt;" not in site.html
    assert "&lt;strong&gt;" not in site.html


def test_save_site_writes_index_html(tmp_path: Path):
    spec = SiteSpec(author_name="Demo Author")
    sections = [GeneratedSection(name="bio", heading="About", body="Author biography.")]
    site = build_html(spec, sections)

    output_path = save_site(site, tmp_path)

    assert output_path.name == "index.html"
    assert output_path.exists()
