from __future__ import annotations

import json
from pathlib import Path

from pydantic import BaseModel, Field

from agentic_site_factory.ingestion import load_local_text_documents
from agentic_site_factory.models import SiteSpec
from agentic_site_factory.pipeline import run_generation_pipeline


class GenerationSpecFile(BaseModel):
    author_name: str
    audience: str
    tone: str
    website_goal: str
    theme: str = "literary"
    requested_sections: list[str] = Field(
        default_factory=lambda: ["hero", "bio", "books", "gallery", "shop", "contact"]
    )
    source_files: list[str]
    output_dir: str


def load_generation_spec(path: Path) -> GenerationSpecFile:
    payload = json.loads(path.read_text(encoding="utf-8"))
    return GenerationSpecFile.model_validate(payload)


def build_site_from_spec_file(spec_path: Path, root: Path | None = None) -> Path:
    project_root = root or Path.cwd()
    generation_spec = load_generation_spec(spec_path)

    source_paths = [
        (project_root / file_name).resolve() for file_name in generation_spec.source_files
    ]
    output_dir = (project_root / generation_spec.output_dir).resolve()

    documents = load_local_text_documents(source_paths)

    site_spec = SiteSpec(
        author_name=generation_spec.author_name,
        audience=generation_spec.audience,
        tone=generation_spec.tone,
        website_goal=generation_spec.website_goal,
        theme=generation_spec.theme,
        requested_sections=generation_spec.requested_sections,
    )

    result = run_generation_pipeline(
        spec=site_spec,
        documents=documents,
        output_dir=output_dir,
        top_k=6,
    )

    if not result.quality_report.passed:
        failed_checks = [
            check.name for check in result.quality_report.checks if not check.passed
        ]
        raise RuntimeError(f"Spec generation failed quality checks: {failed_checks}")

    return output_dir
