from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from agentic_site_factory.agents import generate_sections, plan_site
from agentic_site_factory.artifacts import ArtifactManifest, save_artifact_bundle
from agentic_site_factory.models import GeneratedSite, RetrievedPassage, SitePlan, SiteSpec, SourceDocument
from agentic_site_factory.quality import QualityReport, evaluate_site
from agentic_site_factory.retrieval import retrieve_passages
from agentic_site_factory.site_builder import build_html
from agentic_site_factory.theming import infer_custom_theme


@dataclass(frozen=True)
class GenerationResult:
    spec: SiteSpec
    plan: SitePlan
    passages: list[RetrievedPassage]
    site: GeneratedSite
    quality_report: QualityReport
    manifest: ArtifactManifest | None = None
    output_dir: Path | None = None


def build_query(spec: SiteSpec) -> str:
    return " ".join(
        [
            spec.author_name,
            spec.audience,
            spec.tone,
            spec.website_goal,
            spec.style_guidance,
            " ".join(spec.requested_sections),
        ]
    )


def run_generation_pipeline(
    spec: SiteSpec,
    documents: list[SourceDocument],
    output_dir: Path | None = None,
    top_k: int = 6,
) -> GenerationResult:
    query = build_query(spec)
    passages = retrieve_passages(documents, query=query, top_k=top_k)
    theme = infer_custom_theme(spec, documents, passages)
    plan = plan_site(spec, passages)
    sections = generate_sections(spec, passages)
    site = build_html(spec, sections, theme=theme, documents=documents)
    quality_report = evaluate_site(spec, site, passages)

    manifest = None

    if output_dir is not None:
        manifest = save_artifact_bundle(
            output_dir=output_dir,
            spec=spec,
            plan=plan,
            site=site,
            passages=passages,
            quality_report=quality_report,
        )

    return GenerationResult(
        spec=spec,
        plan=plan,
        passages=passages,
        site=site,
        quality_report=quality_report,
        manifest=manifest,
        output_dir=output_dir,
    )
