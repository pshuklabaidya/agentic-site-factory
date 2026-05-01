from agentic_site_factory.models import GeneratedSection, GeneratedSite, RetrievedPassage, SiteSpec
from agentic_site_factory.quality import evaluate_site
from agentic_site_factory.theming import infer_custom_theme


def test_evaluate_site_passes_for_complete_site():
    spec = SiteSpec(requested_sections=["hero", "shop"])
    theme = infer_custom_theme(spec, [], [])
    sections = [
        GeneratedSection(
            name="hero",
            heading="Hero",
            body="Body",
            evidence_sources=["sample.txt"],
        ),
        GeneratedSection(
            name="shop",
            heading="Shop",
            body="Body",
            evidence_sources=["sample.txt"],
        ),
    ]
    site = GeneratedSite(
        title="Demo",
        html="<!doctype html><header></header><main></main><script>addToCart(); cart-count</script></html>",
        sections=sections,
        theme=theme,
    )
    passages = [RetrievedPassage(source="sample.txt", text="Evidence", score=0.9)]

    report = evaluate_site(spec, site, passages)

    assert report.passed
