from __future__ import annotations

from pathlib import Path

from agentic_site_factory.agents import generate_sections, plan_site
from agentic_site_factory.artifacts import save_artifact_bundle
from agentic_site_factory.ingestion import load_local_text_documents
from agentic_site_factory.models import SiteSpec
from agentic_site_factory.quality import evaluate_site
from agentic_site_factory.retrieval import retrieve_passages
from agentic_site_factory.site_builder import build_html


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

    query = f"{spec.author_name} {spec.audience} {spec.website_goal}"
    passages = retrieve_passages(documents, query=query, top_k=6)
    plan = plan_site(spec, passages)
    sections = generate_sections(spec, passages)
    site = build_html(spec, sections)
    quality_report = evaluate_site(spec, site, passages)

    save_artifact_bundle(
        output_dir=OUTPUT_DIR,
        spec=spec,
        plan=plan,
        site=site,
        passages=passages,
        quality_report=quality_report,
    )

    return OUTPUT_DIR


def main() -> None:
    output_dir = build_demo_site()
    print(f"Demo site generated at: {output_dir}")
    print(f"Open this file: {output_dir / 'index.html'}")


if __name__ == "__main__":
    main()
