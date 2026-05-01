from __future__ import annotations

from pydantic import BaseModel, Field

from agentic_site_factory.models import GeneratedSection, GeneratedSite, RetrievedPassage, SiteSpec


class QualityCheck(BaseModel):
    name: str
    passed: bool
    detail: str


class QualityReport(BaseModel):
    passed: bool
    checks: list[QualityCheck] = Field(default_factory=list)


def required_section_check(spec: SiteSpec, sections: list[GeneratedSection]) -> QualityCheck:
    generated_names = {section.name for section in sections}
    missing = [section for section in spec.requested_sections if section not in generated_names]

    return QualityCheck(
        name="requested_sections_present",
        passed=not missing,
        detail="All requested sections are present." if not missing else f"Missing sections: {missing}",
    )


def evidence_check(passages: list[RetrievedPassage], sections: list[GeneratedSection]) -> QualityCheck:
    if not passages:
        return QualityCheck(
            name="retrieved_evidence_available",
            passed=False,
            detail="No retrieved evidence was available.",
        )

    sections_with_sources = [
        section.name for section in sections if section.evidence_sources
    ]

    return QualityCheck(
        name="section_evidence_sources_present",
        passed=bool(sections_with_sources),
        detail=(
            f"Sections with evidence sources: {sections_with_sources}"
            if sections_with_sources
            else "No sections include evidence source references."
        ),
    )


def html_check(site: GeneratedSite) -> QualityCheck:
    required_fragments = ["<!doctype html>", "<header>", "<main>", "</html>"]
    missing = [fragment for fragment in required_fragments if fragment not in site.html.lower()]

    return QualityCheck(
        name="html_structure_present",
        passed=not missing,
        detail="HTML shell is present." if not missing else f"Missing HTML fragments: {missing}",
    )


def commerce_check(site: GeneratedSite) -> QualityCheck:
    has_cart = "cart-count" in site.html and "addToCart" in site.html

    return QualityCheck(
        name="demo_commerce_present",
        passed=has_cart,
        detail="Demo cart interaction is present." if has_cart else "Demo cart interaction is missing.",
    )


def evaluate_site(
    spec: SiteSpec,
    site: GeneratedSite,
    passages: list[RetrievedPassage],
) -> QualityReport:
    checks = [
        required_section_check(spec, site.sections),
        evidence_check(passages, site.sections),
        html_check(site),
        commerce_check(site),
    ]

    return QualityReport(
        passed=all(check.passed for check in checks),
        checks=checks,
    )
