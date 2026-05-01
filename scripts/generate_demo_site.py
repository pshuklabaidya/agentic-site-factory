from __future__ import annotations

from pathlib import Path

from agentic_site_factory.ingestion import load_local_text_documents
from agentic_site_factory.models import SiteSpec
from agentic_site_factory.pipeline import run_generation_pipeline


ROOT = Path(__file__).resolve().parents[1]
SAMPLE_PATH = ROOT / "data" / "sample_manuscripts" / "elena_vale.txt"
OUTPUT_DIR = ROOT / "generated_sites" / "demo_cli"


def build_demo_site() -> Path:
    documents = load_local_text_documents([SAMPLE_PATH])

    spec = SiteSpec(
        author_name="Elena Vale",
        audience="literary fiction readers and book clubs",
        tone="warm, elegant, and immersive",
        website_goal=(
            "Introduce the author, showcase books, and help readers explore and purchase "
            "featured titles."
        ),
        requested_sections=["hero", "bio", "books", "gallery", "shop", "contact"],
    )

    result = run_generation_pipeline(
        spec=spec,
        documents=documents,
        output_dir=OUTPUT_DIR,
        top_k=6,
    )

    if not result.quality_report.passed:
        failed_checks = [
            check.name for check in result.quality_report.checks if not check.passed
        ]
        raise RuntimeError(f"Demo generation failed quality checks: {failed_checks}")

    return OUTPUT_DIR


def main() -> None:
    output_dir = build_demo_site()
    print(f"Demo site generated at: {output_dir}")
    print(f"Open this file: {output_dir / 'index.html'}")


if __name__ == "__main__":
    main()
