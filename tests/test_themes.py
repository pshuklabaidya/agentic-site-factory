from agentic_site_factory.models import GeneratedSection, SiteSpec
from agentic_site_factory.site_builder import build_html, resolve_theme


def test_resolve_theme_falls_back_to_literary():
    assert resolve_theme("unknown") == resolve_theme("literary")


def test_build_html_uses_modern_theme_values():
    spec = SiteSpec(author_name="Demo Author", theme="modern")
    sections = [GeneratedSection(name="hero", heading="Hero", body="Body")]

    site = build_html(spec, sections)

    assert "#2563eb" in site.html
    assert "Demo Author" in site.html
