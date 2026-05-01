from pathlib import Path

from agentic_site_factory.models import GeneratedSection, SiteSpec
from agentic_site_factory.site_builder import build_html, save_site


def test_build_html_contains_author_name():
    spec = SiteSpec(author_name="Demo Author")
    sections = [GeneratedSection(name="bio", heading="About", body="Author biography.")]

    site = build_html(spec, sections)

    assert "Demo Author" in site.html
    assert "Author biography." in site.html
    assert site.theme.name


def test_save_site_writes_index_html(tmp_path: Path):
    spec = SiteSpec(author_name="Demo Author")
    sections = [GeneratedSection(name="bio", heading="About", body="Author biography.")]
    site = build_html(spec, sections)

    output_path = save_site(site, tmp_path)

    assert output_path.name == "index.html"
    assert output_path.exists()
