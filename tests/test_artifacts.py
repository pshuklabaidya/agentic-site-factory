from agentic_site_factory.artifacts import save_artifact_bundle
from agentic_site_factory.models import GeneratedSection, GeneratedSite, RetrievedPassage, SitePlan, SiteSpec
from agentic_site_factory.quality import evaluate_site
from agentic_site_factory.theming import infer_custom_theme


def test_save_artifact_bundle_writes_expected_files(tmp_path):
    spec = SiteSpec(author_name="Demo Author", requested_sections=["hero"])
    theme = infer_custom_theme(spec, [], [])
    plan = SitePlan(
        title="Demo Site",
        sections=["hero"],
        content_strategy="Use evidence.",
        agent_steps=["Plan", "Build"],
    )
    site = GeneratedSite(
        title="Demo Site",
        html="<!doctype html><header></header><main></main><script>addToCart(); cart-count</script></html>",
        sections=[
            GeneratedSection(
                name="hero",
                heading="Hero",
                body="Body",
                evidence_sources=["source.txt"],
            )
        ],
        theme=theme,
    )
    passages = [RetrievedPassage(source="source.txt", text="Evidence", score=1.0)]
    quality_report = evaluate_site(spec, site, passages)

    manifest = save_artifact_bundle(
        output_dir=tmp_path,
        spec=spec,
        plan=plan,
        site=site,
        passages=passages,
        quality_report=quality_report,
    )

    assert manifest.quality_passed
    assert (tmp_path / "index.html").exists()
    assert (tmp_path / "site_plan.json").exists()
    assert (tmp_path / "evidence_map.json").exists()
    assert (tmp_path / "quality_report.json").exists()
    assert (tmp_path / "theme_spec.json").exists()
    assert (tmp_path / "artifact_manifest.json").exists()
