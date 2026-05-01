from pathlib import Path

from agentic_site_factory.models import SiteSpec, SourceDocument
from agentic_site_factory.pipeline import GenerationResult, run_generation_pipeline


def test_generation_result_model_imports():
    assert GenerationResult is not None


def test_run_generation_pipeline_returns_complete_result(tmp_path: Path):
    spec = SiteSpec(
        author_name="Demo Author",
        audience="readers",
        tone="warm",
        website_goal="introduce books",
        requested_sections=["hero", "books", "shop"],
    )
    documents = [
        SourceDocument(
            name="sample_book_manuscript.txt",
            text="Chapter One. A warm book about memory, books, readers, and coastal stories.",
        )
    ]

    result = run_generation_pipeline(
        spec=spec,
        documents=documents,
        output_dir=tmp_path,
        top_k=3,
    )

    assert result.site.title == "Demo Author - Official Author Site"
    assert result.plan.sections == ["hero", "books", "shop"]
    assert result.quality_report.passed
    assert result.manifest is not None
    assert (tmp_path / "index.html").exists()
    assert (tmp_path / "books.html").exists()
    assert (tmp_path / "book-sample-book-manuscript.html").exists()
