from agentic_site_factory.models import RetrievedPassage, SiteSpec, SourceDocument
from agentic_site_factory.theming import infer_custom_theme, select_style_family


def test_select_style_family_prefers_scholarly_for_theology_signals():
    variant = select_style_family(
        SiteSpec(
            author_name="Prashant",
            tone="confessional biblical theology",
            website_goal="Teach doctrine through rich theological study.",
            style_guidance="scholarly and classic",
        ),
        [SourceDocument(name="lesson.txt", text="A theological study in doctrine, exegesis, and confessional analysis.")],
        [RetrievedPassage(source="lesson.txt", text="biblical exegesis and doctrine", score=0.8)],
    )

    assert variant == "scholarly-classic"


def test_infer_custom_theme_returns_variant_and_palette():
    theme = infer_custom_theme(
        SiteSpec(
            author_name="Elena Vale",
            tone="warm, elegant, immersive literary fiction",
            website_goal="Showcase novels and invite readers into reflective stories.",
            style_guidance="editorial, bookish, intimate",
        ),
        [SourceDocument(name="novel.txt", text="A literary novel about family, memory, and handwritten letters.")],
        [RetrievedPassage(source="novel.txt", text="lyrical coastal story", score=0.9)],
    )

    assert theme.variant == "editorial-warm"
    assert theme.background
    assert theme.cover_gradient
