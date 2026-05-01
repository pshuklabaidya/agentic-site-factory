from agentic_site_factory.models import RetrievedPassage, SiteSpec, SourceDocument
from agentic_site_factory.site_builder import build_html
from agentic_site_factory.theming import infer_custom_theme


def test_infer_custom_theme_changes_with_inputs():
    literary_spec = SiteSpec(
        author_name="Elena Vale",
        tone="warm, elegant, immersive literary fiction",
        website_goal="Showcase novels and invite readers into reflective stories.",
        style_guidance="editorial, bookish, intimate",
    )
    modern_spec = SiteSpec(
        author_name="Nova Metrics",
        tone="clean, modern, sharp",
        website_goal="Present an AI consultancy and product dashboard.",
        style_guidance="minimal, sleek, startup",
    )

    literary_theme = infer_custom_theme(
        literary_spec,
        [SourceDocument(name="novel.txt", text="A literary novel about family, memory, and handwritten letters.")],
        [RetrievedPassage(source="novel.txt", text="lyrical coastal story", score=0.9)],
    )
    modern_theme = infer_custom_theme(
        modern_spec,
        [SourceDocument(name="product.txt", text="A modern AI dashboard for product analytics and consulting.")],
        [RetrievedPassage(source="product.txt", text="clean startup interface", score=0.9)],
    )

    assert literary_theme.variant != modern_theme.variant
    assert literary_theme.background != modern_theme.background
    assert literary_theme.font_family != modern_theme.font_family


def test_build_html_uses_responsive_site_title_class_and_theme_variant():
    site = build_html(
        SiteSpec(author_name="Prashant Shuklabaidya"),
        [],
    )

    assert 'class="site-title"' in site.html
    assert 'body class="theme-' in site.html
    assert "text-wrap: balance;" in site.html
    assert "overflow-wrap: anywhere;" in site.html
