from __future__ import annotations

from textwrap import shorten

from openai import OpenAI, OpenAIError

from agentic_site_factory.models import GeneratedSection, RetrievedPassage, SitePlan, SiteSpec
from agentic_site_factory.settings import load_openai_settings
from agentic_site_factory.text_sanitizer import sanitize_body, sanitize_heading


def openai_available() -> bool:
    return load_openai_settings().enabled


def openai_model_name() -> str:
    return load_openai_settings().model


def plan_site(spec: SiteSpec, passages: list[RetrievedPassage]) -> SitePlan:
    evidence_preview = " ".join(passage.text for passage in passages[:3])
    shortened_evidence = shorten(evidence_preview, width=420, placeholder="...")

    strategy = (
        f"Build a {spec.tone} website for {spec.author_name}, aimed at {spec.audience}. "
        f"The site should {spec.website_goal}. "
        f"Concrete claims should be grounded in manuscript evidence such as: {shortened_evidence}"
    )

    return SitePlan(
        title=f"{spec.author_name} - Official Author Site",
        sections=spec.requested_sections,
        content_strategy=strategy,
        agent_steps=[
            "Intake agent normalizes the site specification.",
            "Retrieval agent selects source-grounded passages from manuscript material.",
            "Planner agent maps requested sections to page responsibilities.",
            "Writer agent creates concise website copy from retrieved evidence.",
            "Builder agent renders a static HTML artifact for preview and download.",
        ],
    )


def summarize_evidence(passages: list[RetrievedPassage], width: int = 520) -> str:
    combined = " ".join(passage.text for passage in passages[:2])

    if not combined:
        return "No manuscript evidence was supplied."

    return shorten(combined, width=width, placeholder="...")


def generate_section_deterministic(
    section_name: str,
    spec: SiteSpec,
    passages: list[RetrievedPassage],
) -> GeneratedSection:
    summary = summarize_evidence(passages)
    sources = sorted({passage.source for passage in passages if passage.source})

    headings = {
        "hero": f"Meet {spec.author_name}",
        "bio": "About the Author",
        "books": "Featured Books",
        "gallery": "Gallery",
        "shop": "Bookstore",
        "contact": "Connect",
    }

    bodies = {
        "hero": (
            f"{spec.author_name} writes for {spec.audience} in a {spec.tone} voice. "
            "The site invites readers into the world of the books and the themes that shape them."
        ),
        "bio": (
            f"{spec.author_name} is introduced through themes drawn from the supplied material: "
            f"{summary}"
        ),
        "books": (
            "The featured catalog highlights central images, conflicts, promises, and reader "
            f"experience present in the manuscript evidence: {summary}"
        ),
        "gallery": (
            "The gallery is designed for book covers, launch images, event photos, writing spaces, "
            "and visual motifs connected to the books."
        ),
        "shop": (
            "The shop section presents featured titles with demo purchase actions that can later "
            "connect to Stripe, Shopify, Gumroad, or another commerce provider."
        ),
        "contact": (
            "Readers, reviewers, bookstores, podcasters, and event organizers can use this section "
            "to request interviews, visits, reviews, and updates."
        ),
    }

    return GeneratedSection(
        name=section_name,
        heading=headings.get(section_name, section_name.title()),
        body=bodies.get(
            section_name,
            f"This section supports the site goal: {spec.website_goal}. Evidence basis: {summary}",
        ),
        evidence_sources=sources,
    )


def parse_heading_body(text: str, fallback_heading: str) -> tuple[str, str]:
    heading = fallback_heading
    body_lines: list[str] = []

    for line in text.splitlines():
        stripped = line.strip()

        if stripped.lower().startswith("heading:"):
            heading = stripped.split(":", 1)[1].strip() or fallback_heading
        elif stripped.lower().startswith("body:"):
            body_lines.append(stripped.split(":", 1)[1].strip())
        elif stripped:
            body_lines.append(stripped)

    body = " ".join(body_lines).strip() or text.strip()
    return heading, body


def generate_section_with_openai(
    section_name: str,
    spec: SiteSpec,
    passages: list[RetrievedPassage],
) -> GeneratedSection:
    settings = load_openai_settings()

    if not settings.enabled:
        return generate_section_deterministic(section_name, spec, passages)

    evidence = "\n\n".join(
        f"Source: {passage.source}\nPassage: {passage.text}" for passage in passages[:5]
    )

    prompt = f"""
Create concise website copy for one section of an author or creator website.

Author or brand: {spec.author_name}
Audience: {spec.audience}
Tone: {spec.tone}
Website goal: {spec.website_goal}
Optional style guidance: {spec.style_guidance}
Section: {section_name}

Use only the supplied evidence for concrete claims.
Keep the body under 120 words.
Do not invent titles, biography facts, awards, prices, dates, publishers, or purchase links.

Evidence:
{evidence}

Return exactly two labeled fields:
Heading: <heading>
Body: <body>
""".strip()

    try:
        client = OpenAI(api_key=settings.api_key, timeout=20.0, max_retries=0)
        response = client.responses.create(
            model=settings.model,
            input=[
                {
                    "role": "system",
                    "content": "Write grounded website copy from supplied evidence.",
                },
                {"role": "user", "content": prompt},
            ],
        )
        text = response.output_text.strip()
    except OpenAIError:
        return generate_section_deterministic(section_name, spec, passages)

    heading, body = parse_heading_body(text, section_name.title())
    heading = sanitize_heading(heading, fallback=section_name.title())
    body = sanitize_body(body)
    sources = sorted({passage.source for passage in passages if passage.source})

    return GeneratedSection(
        name=section_name,
        heading=heading,
        body=body,
        evidence_sources=sources,
    )


def generate_sections(spec: SiteSpec, passages: list[RetrievedPassage]) -> list[GeneratedSection]:
    return [
        generate_section_with_openai(section_name, spec, passages)
        for section_name in spec.requested_sections
    ]
