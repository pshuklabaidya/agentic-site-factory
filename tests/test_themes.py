from agentic_site_factory.models import GeneratedSection, SiteSpec, ThemeSpec
from agentic_site_factory.site_builder import build_html


def test_build_html_uses_supplied_custom_theme_values():
    spec = SiteSpec(author_name="Demo Author")
    sections = [GeneratedSection(name="hero", heading="Hero", body="Body")]
    theme = ThemeSpec(
        name="Custom Test",
        rationale="Test rationale.",
        font_family="Inter, Arial, sans-serif",
        background="#ffffff",
        ink="#111111",
        muted="#555555",
        card="#f8f8f8",
        accent="#123456",
        accent_soft="#ddeeff",
        border="#cccccc",
        cover_gradient="linear-gradient(135deg, #111111, #123456)",
    )

    site = build_html(spec, sections, theme=theme)

    assert "#123456" in site.html
    assert "Demo Author" in site.html
    assert site.theme.name == "Custom Test"
