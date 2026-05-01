from __future__ import annotations

from pydantic import BaseModel

from agentic_site_factory.models import GeneratedSite, RetrievedPassage, SiteSpec


class QualityCheck(BaseModel):
    name: str
    passed: bool
    detail: str


class QualityReport(BaseModel):
    passed: bool
    checks: list[QualityCheck]


def check_requested_sections_present(spec: SiteSpec, site: GeneratedSite) -> QualityCheck:
    html_blob = "\n".join(site.pages.values()) if site.pages else site.html
    missing_sections = [
        section for section in spec.requested_sections if section.lower() not in html_blob.lower()
    ]

    if missing_sections:
        return QualityCheck(
            name="requested_sections_present",
            passed=False,
            detail=f"Missing requested sections: {', '.join(missing_sections)}",
        )

    return QualityCheck(
        name="requested_sections_present",
        passed=True,
        detail="All requested sections are present.",
    )


def check_grounding_visible(passages: list[RetrievedPassage], site: GeneratedSite) -> QualityCheck:
    html_blob = "\n".join(site.pages.values()) if site.pages else site.html

    if not passages:
        return QualityCheck(
            name="grounding_visible",
            passed=False,
            detail="No retrieved passages were available.",
        )

    source_names = {passage.source for passage in passages if passage.source}
    visible_sources = [source for source in source_names if source in html_blob]

    if not visible_sources:
        return QualityCheck(
            name="grounding_visible",
            passed=False,
            detail="Retrieved evidence sources are not visible in generated artifacts.",
        )

    return QualityCheck(
        name="grounding_visible",
        passed=True,
        detail="Retrieved evidence sources are visible.",
    )


def check_static_html_present(site: GeneratedSite) -> QualityCheck:
    html_blob = "\n".join(site.pages.values()) if site.pages else site.html
    required_fragments = ["<!doctype html>", "<html", "<head", "<body", "<main"]

    missing_fragments = [
        fragment for fragment in required_fragments if fragment.lower() not in html_blob.lower()
    ]

    if missing_fragments:
        return QualityCheck(
            name="static_html_present",
            passed=False,
            detail=f"Missing HTML fragments: {', '.join(missing_fragments)}",
        )

    return QualityCheck(
        name="static_html_present",
        passed=True,
        detail="Static HTML shell is present.",
    )


def check_demo_commerce_present(spec: SiteSpec, site: GeneratedSite) -> QualityCheck:
    html_blob = "\n".join(site.pages.values()) if site.pages else site.html

    commerce_requested = any(
        section in {"shop", "books"} for section in spec.requested_sections
    )

    if not commerce_requested:
        return QualityCheck(
            name="demo_commerce_present",
            passed=True,
            detail="Commerce interaction was not requested.",
        )

    has_legacy_cart = "addToCart" in html_blob and "cart-count" in html_blob
    has_persistent_book_cart = (
        "addBookToCart" in html_blob
        and "agenticSiteFactoryCart" in html_blob
        and "localStorage.setItem" in html_blob
        and "cart-count" in html_blob
    )

    if has_legacy_cart or has_persistent_book_cart:
        return QualityCheck(
            name="demo_commerce_present",
            passed=True,
            detail="Persistent demo cart interaction is present.",
        )

    return QualityCheck(
        name="demo_commerce_present",
        passed=False,
        detail="Demo cart interaction is missing.",
    )


def evaluate_site(
    spec: SiteSpec,
    site: GeneratedSite,
    passages: list[RetrievedPassage],
) -> QualityReport:
    checks = [
        check_requested_sections_present(spec, site),
        check_grounding_visible(passages, site),
        check_static_html_present(site),
        check_demo_commerce_present(spec, site),
    ]

    return QualityReport(
        passed=all(check.passed for check in checks),
        checks=checks,
    )
