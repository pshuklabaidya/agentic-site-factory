from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from pydantic import BaseModel, Field

from agentic_site_factory.models import GeneratedSite, RetrievedPassage, SitePlan, SiteSpec
from agentic_site_factory.quality import QualityReport


class ArtifactManifest(BaseModel):
    project_name: str = "Agentic Site Factory"
    site_title: str
    author_name: str
    requested_sections: list[str]
    generated_sections: list[str]
    inferred_theme_name: str
    inferred_theme_rationale: str
    evidence_sources: list[str]
    quality_passed: bool
    files: list[str] = Field(default_factory=list)


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def save_artifact_bundle(
    output_dir: Path,
    spec: SiteSpec,
    plan: SitePlan,
    site: GeneratedSite,
    passages: list[RetrievedPassage],
    quality_report: QualityReport,
) -> ArtifactManifest:
    output_dir.mkdir(parents=True, exist_ok=True)

    index_path = output_dir / "index.html"
    plan_path = output_dir / "site_plan.json"
    evidence_path = output_dir / "evidence_map.json"
    quality_path = output_dir / "quality_report.json"
    theme_path = output_dir / "theme_spec.json"
    manifest_path = output_dir / "artifact_manifest.json"

    index_path.write_text(site.html, encoding="utf-8")

    write_json(plan_path, plan.model_dump())
    write_json(
        evidence_path,
        {
            "retrieved_passages": [passage.model_dump() for passage in passages],
            "section_sources": {
                section.name: section.evidence_sources for section in site.sections
            },
        },
    )
    write_json(quality_path, quality_report.model_dump())
    write_json(theme_path, site.theme.model_dump())

    evidence_sources = sorted({passage.source for passage in passages if passage.source})
    manifest = ArtifactManifest(
        site_title=site.title,
        author_name=spec.author_name,
        requested_sections=spec.requested_sections,
        generated_sections=[section.name for section in site.sections],
        inferred_theme_name=site.theme.name,
        inferred_theme_rationale=site.theme.rationale,
        evidence_sources=evidence_sources,
        quality_passed=quality_report.passed,
        files=[
            index_path.name,
            plan_path.name,
            evidence_path.name,
            quality_path.name,
            theme_path.name,
            manifest_path.name,
        ],
    )

    write_json(manifest_path, manifest.model_dump())

    return manifest
