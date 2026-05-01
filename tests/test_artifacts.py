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
    html = """
    <!doctype html>
    <html>
      <head><title>Demo Site</title></head>
      <body>
        <main>
          <section id="hero">
            <div class="section-label">Hero Agent</div>
            <h2>Hero</h2>
            <p>Body</p>
            <p class="source-note">Grounded in: source.txt</p>
          </section>
          <aside class="cart-panel">
            <span id="cart-count">0</span>
            <ul id="cart-items"></ul>
          </aside>
          <script>
            function addBookToCart(book) {
              const current = JSON.parse(localStorage.getItem("agenticSiteFactoryCart") || "[]");
              localStorage.setItem("agenticSiteFactoryCart", JSON.stringify(current));
            }
          </script>
        </main>
      </body>
    </html>
    """
    site = GeneratedSite(
        title="Demo Site",
        html=html,
        sections=[
            GeneratedSection(
                name="hero",
                heading="Hero",
                body="Body",
                evidence_sources=["source.txt"],
            )
        ],
        theme=theme,
        pages={"index.html": html, "hero.html": html},
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
    assert (tmp_path / "hero.html").exists()
    assert (tmp_path / "site_plan.json").exists()
    assert (tmp_path / "evidence_map.json").exists()
    assert (tmp_path / "quality_report.json").exists()
    assert (tmp_path / "theme_spec.json").exists()
    assert (tmp_path / "artifact_manifest.json").exists()
    assert "hero.html" in manifest.files
