from agentic_site_factory.models import SiteSpec, SourceDocument
from agentic_site_factory.pipeline import build_query, run_generation_pipeline


def test_build_query_contains_site_spec_fields():
    spec = SiteSpec(
        author_name="Demo Author",
        audience="book clubs",
        tone="warm",
        website_goal="sell books",
        requested_sections=["hero", "shop"],
    )

    query = build_query(spec)

    assert "Demo Author" in query
    assert "book clubs" in query
    assert "sell books" in query
    assert "shop" in query


def test_run_generation_pipeline_returns_complete_result(tmp_path):
    spec = SiteSpec(
        author_name="Demo Author",
        audience="readers",
        tone="warm",
        website_goal="introduce books",
        requested_sections=["hero", "shop"],
    )
    documents = [
        SourceDocument(
            name="sample.txt",
            text="A warm author biography about memory, books, readers, and coastal stories.",
        )
    ]

    result = run_generation_pipeline(
        spec=spec,
        documents=documents,
        output_dir=tmp_path,
        top_k=3,
    )

    assert result.plan.title == "Demo Author - Official Author Site"
    assert result.passages
    assert result.site.html
    assert result.quality_report.passed
    assert result.manifest is not None
    assert (tmp_path / "index.html").exists()
