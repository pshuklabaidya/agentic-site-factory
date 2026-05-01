from agentic_site_factory.models import SiteSpec, SourceDocument
from agentic_site_factory.theming import infer_custom_theme, select_style_family


def test_select_style_family_defaults_to_literary():
    assert select_style_family("") == "literary"


def test_infer_custom_theme_uses_business_material():
    spec = SiteSpec(
        audience="startup founders",
        website_goal="Promote consulting services and technology strategy.",
    )
    documents = [
        SourceDocument(
            name="sample.txt",
            text="This business uses AI, analytics, software, product strategy, and SaaS dashboards.",
        )
    ]

    theme = infer_custom_theme(spec, documents, [])

    assert theme.name == "Modern Product"
    assert theme.accent == "#2563eb"


def test_infer_custom_theme_uses_dark_material():
    spec = SiteSpec()
    documents = [
        SourceDocument(
            name="sample.txt",
            text="A noir thriller about night, shadow, mystery, and suspense.",
        )
    ]

    theme = infer_custom_theme(spec, documents, [])

    assert theme.name == "Noir Dramatic"


def test_style_guidance_participates_in_inference():
    spec = SiteSpec(style_guidance="luxury boutique elegant premium gallery")
    documents = [SourceDocument(name="sample.txt", text="A short author profile.")]

    theme = infer_custom_theme(spec, documents, [])

    assert theme.name == "Refined Boutique"
