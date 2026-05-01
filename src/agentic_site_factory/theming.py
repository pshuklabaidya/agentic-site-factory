from __future__ import annotations

from collections import Counter

from agentic_site_factory.models import RetrievedPassage, SiteSpec, SourceDocument, ThemeSpec


STYLE_SIGNALS = {
    "literary": [
        "author",
        "book",
        "book club",
        "chapter",
        "coastal",
        "essay",
        "family",
        "fiction",
        "letters",
        "literary",
        "lyrical",
        "manuscript",
        "memoir",
        "memory",
        "novel",
        "poetry",
        "readers",
        "reconciliation",
        "story",
    ],
    "modern": [
        "ai",
        "analytics",
        "brand",
        "business",
        "consulting",
        "dashboard",
        "data",
        "founder",
        "innovation",
        "product",
        "professional",
        "saas",
        "service",
        "software",
        "startup",
        "strategy",
        "technology",
    ],
    "dark": [
        "crime",
        "cyberpunk",
        "dark",
        "dystopian",
        "gothic",
        "horror",
        "midnight",
        "mystery",
        "night",
        "noir",
        "shadow",
        "suspense",
        "thriller",
    ],
    "earthy": [
        "artisan",
        "bakery",
        "craft",
        "earth",
        "farm",
        "food",
        "garden",
        "handmade",
        "hearth",
        "kitchen",
        "meal",
        "natural",
        "organic",
        "soil",
        "warmth",
        "wood",
    ],
    "luxury": [
        "boutique",
        "elegant",
        "executive",
        "gallery",
        "gold",
        "luxury",
        "premium",
        "refined",
        "signature",
        "studio",
        "tailored",
    ],
}


STYLE_RECIPES = {
    "literary": {
        "name": "Atmospheric Literary",
        "font_family": "Georgia, serif",
        "background": "#f8f5ef",
        "ink": "#1f2933",
        "muted": "#667085",
        "card": "#ffffff",
        "accent": "#6d28d9",
        "accent_soft": "#eee7ff",
        "border": "#e6e0d6",
        "cover_gradient": "linear-gradient(135deg, #1f2933, #6d28d9)",
    },
    "modern": {
        "name": "Modern Product",
        "font_family": "Inter, Arial, sans-serif",
        "background": "#f5f7fb",
        "ink": "#111827",
        "muted": "#64748b",
        "card": "#ffffff",
        "accent": "#2563eb",
        "accent_soft": "#dbeafe",
        "border": "#dbe3ef",
        "cover_gradient": "linear-gradient(135deg, #0f172a, #2563eb)",
    },
    "dark": {
        "name": "Noir Dramatic",
        "font_family": "Inter, Arial, sans-serif",
        "background": "#0f172a",
        "ink": "#f8fafc",
        "muted": "#cbd5e1",
        "card": "#111827",
        "accent": "#a78bfa",
        "accent_soft": "#312e81",
        "border": "#334155",
        "cover_gradient": "linear-gradient(135deg, #4c1d95, #0f172a)",
    },
    "earthy": {
        "name": "Earthy Artisan",
        "font_family": "Georgia, serif",
        "background": "#fbf7ef",
        "ink": "#292524",
        "muted": "#78716c",
        "card": "#fffaf0",
        "accent": "#b45309",
        "accent_soft": "#fed7aa",
        "border": "#e7d8bf",
        "cover_gradient": "linear-gradient(135deg, #78350f, #b45309)",
    },
    "luxury": {
        "name": "Refined Boutique",
        "font_family": "Georgia, serif",
        "background": "#f7f3ee",
        "ink": "#1c1917",
        "muted": "#78716c",
        "card": "#fffdf8",
        "accent": "#92400e",
        "accent_soft": "#fde68a",
        "border": "#e7d8bf",
        "cover_gradient": "linear-gradient(135deg, #1c1917, #92400e)",
    },
}


def combined_style_text(
    spec: SiteSpec,
    documents: list[SourceDocument],
    passages: list[RetrievedPassage],
) -> str:
    document_preview = " ".join(document.text[:2000] for document in documents[:6])
    passage_preview = " ".join(passage.text[:1000] for passage in passages[:6])

    return " ".join(
        [
            spec.author_name,
            spec.audience,
            spec.tone,
            spec.website_goal,
            spec.style_guidance,
            " ".join(spec.requested_sections),
            document_preview,
            passage_preview,
        ]
    ).lower()


def score_style_families(text: str) -> Counter[str]:
    scores: Counter[str] = Counter()

    for family, keywords in STYLE_SIGNALS.items():
        for keyword in keywords:
            if keyword in text:
                scores[family] += 1

    return scores


def select_style_family(text: str) -> str:
    scores = score_style_families(text)

    if not scores:
        return "literary"

    if scores["dark"] >= 2 and scores["dark"] >= scores["modern"]:
        return "dark"

    if scores["modern"] >= 2 and scores["modern"] >= scores["literary"]:
        return "modern"

    if scores["luxury"] >= 2:
        return "luxury"

    if scores["earthy"] >= 2:
        return "earthy"

    return scores.most_common(1)[0][0]


def infer_custom_theme(
    spec: SiteSpec,
    documents: list[SourceDocument],
    passages: list[RetrievedPassage],
) -> ThemeSpec:
    text = combined_style_text(spec, documents, passages)
    family = select_style_family(text)
    recipe = STYLE_RECIPES[family]

    guidance = spec.style_guidance.strip()
    if guidance:
        rationale = (
            f"Derived from provided style guidance and source material. "
            f"Primary visual family: {recipe['name']}."
        )
    else:
        rationale = (
            f"Derived from audience, tone, website goal, retrieved evidence, and uploaded "
            f"source material. Primary visual family: {recipe['name']}."
        )

    return ThemeSpec(
        name=recipe["name"],
        rationale=rationale,
        font_family=recipe["font_family"],
        background=recipe["background"],
        ink=recipe["ink"],
        muted=recipe["muted"],
        card=recipe["card"],
        accent=recipe["accent"],
        accent_soft=recipe["accent_soft"],
        border=recipe["border"],
        cover_gradient=recipe["cover_gradient"],
    )
