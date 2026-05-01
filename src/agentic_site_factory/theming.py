from __future__ import annotations

import re
from collections import defaultdict

from agentic_site_factory.models import RetrievedPassage, SiteSpec, SourceDocument, ThemeSpec


THEME_PRESETS = {
    "editorial-warm": {
        "name": "Editorial Warm",
        "font_family": "Georgia, Garamond, 'Times New Roman', serif",
        "background": "#f4ecd8",
        "ink": "#1f2937",
        "muted": "#6b7280",
        "card": "#fffaf0",
        "accent": "#8b5e3c",
        "accent_soft": "#efe2c4",
        "border": "#d7c7a7",
        "cover_gradient": "linear-gradient(135deg, #8b5e3c, #c58b55)",
    },
    "modern-clean": {
        "name": "Modern Clean",
        "font_family": "Inter, 'Helvetica Neue', Arial, sans-serif",
        "background": "#f3f7fb",
        "ink": "#0f172a",
        "muted": "#475569",
        "card": "#ffffff",
        "accent": "#2563eb",
        "accent_soft": "#dbeafe",
        "border": "#cbd5e1",
        "cover_gradient": "linear-gradient(135deg, #1d4ed8, #38bdf8)",
    },
    "dramatic-dark": {
        "name": "Dramatic Dark",
        "font_family": "Cormorant Garamond, Georgia, serif",
        "background": "#111827",
        "ink": "#f9fafb",
        "muted": "#cbd5e1",
        "card": "#1f2937",
        "accent": "#d4a373",
        "accent_soft": "#2b3548",
        "border": "#374151",
        "cover_gradient": "linear-gradient(135deg, #7c2d12, #d4a373)",
    },
    "scholarly-classic": {
        "name": "Scholarly Classic",
        "font_family": "Charter, Georgia, 'Times New Roman', serif",
        "background": "#f7f4ee",
        "ink": "#1e293b",
        "muted": "#64748b",
        "card": "#ffffff",
        "accent": "#1d4e89",
        "accent_soft": "#dde8f5",
        "border": "#cbd5e1",
        "cover_gradient": "linear-gradient(135deg, #1d4e89, #4f86c6)",
    },
    "playful-bright": {
        "name": "Playful Bright",
        "font_family": "'Avenir Next', 'Trebuchet MS', Arial, sans-serif",
        "background": "#fff7ed",
        "ink": "#422006",
        "muted": "#7c5e3d",
        "card": "#ffffff",
        "accent": "#ea580c",
        "accent_soft": "#ffedd5",
        "border": "#fdba74",
        "cover_gradient": "linear-gradient(135deg, #f97316, #facc15)",
    },
}

AXIS_KEYWORDS = {
    "editorial-warm": [
        "literary", "novel", "story", "stories", "memoir", "lyrical", "family",
        "memory", "coastal", "letters", "readers", "books", "immersive",
        "author", "fiction", "manuscript", "warm", "elegant", "intimate",
    ],
    "modern-clean": [
        "modern", "minimal", "clean", "sharp", "startup", "dashboard", "analytics",
        "ai", "consulting", "product", "technology", "sleek", "professional",
        "contemporary", "digital", "interface",
    ],
    "dramatic-dark": [
        "dark", "gothic", "grief", "mystery", "haunting", "shadow", "night",
        "storm", "loss", "ashes", "blood", "silence", "wound", "noir",
    ],
    "scholarly-classic": [
        "theology", "biblical", "confessional", "academic", "research", "study",
        "doctrine", "historical", "analysis", "scholar", "argument", "exegesis",
        "lecture", "sermon", "thesis",
    ],
    "playful-bright": [
        "children", "young", "adventure", "wonder", "joy", "playful", "bright",
        "imaginative", "colorful", "whimsy", "whimsical",
    ],
}


def collect_signal_text(
    spec: SiteSpec,
    documents: list[SourceDocument],
    passages: list[RetrievedPassage],
) -> str:
    parts: list[str] = [
        spec.author_name,
        spec.audience,
        spec.tone,
        spec.website_goal,
        spec.style_guidance,
        " ".join(spec.requested_sections),
    ]

    for document in documents[:8]:
        parts.append(document.name)
        parts.append(document.text[:6000])

    for passage in passages[:8]:
        parts.append(passage.source)
        parts.append(passage.text[:1200])

    return " ".join(part for part in parts if part).lower()


def score_variants(text: str) -> dict[str, float]:
    scores: dict[str, float] = defaultdict(float)

    for variant, keywords in AXIS_KEYWORDS.items():
        for keyword in keywords:
            scores[variant] += len(re.findall(r"\b" + re.escape(keyword) + r"\b", text))

    if "theology" in text or "confessional" in text or "biblical" in text:
        scores["scholarly-classic"] += 4

    if "dashboard" in text or "analytics" in text or "ai" in text:
        scores["modern-clean"] += 4

    if "novel" in text or "manuscript" in text or "lyrical" in text:
        scores["editorial-warm"] += 4

    if "gothic" in text or "dark" in text or "grief" in text:
        scores["dramatic-dark"] += 4

    if "children" in text or "adventure" in text or "playful" in text:
        scores["playful-bright"] += 4

    if not any(scores.values()):
        scores["editorial-warm"] = 1

    return scores


def select_style_family(
    spec_or_text: SiteSpec | str,
    documents: list[SourceDocument] | None = None,
    passages: list[RetrievedPassage] | None = None,
) -> str:
    if isinstance(spec_or_text, str):
        text = spec_or_text.lower()
    else:
        text = collect_signal_text(spec_or_text, documents or [], passages or [])

    scores = score_variants(text)
    return max(scores, key=scores.get)


def build_rationale(variant: str, spec: SiteSpec, documents: list[SourceDocument]) -> str:
    signals = []
    if spec.style_guidance.strip():
        signals.append("style guidance")
    if spec.tone.strip():
        signals.append("tone")
    if spec.website_goal.strip():
        signals.append("site goal")
    if documents:
        signals.append("uploaded documents")

    signal_text = ", ".join(signals) if signals else "default signals"

    rationale_map = {
        "editorial-warm": "bookish, reflective, and human-centered signals",
        "modern-clean": "minimal, digital, and contemporary brand signals",
        "dramatic-dark": "moody, high-contrast, and dramatic narrative signals",
        "scholarly-classic": "academic, confessional, and archival signals",
        "playful-bright": "bright, energetic, and imaginative signals",
    }

    return f"Derived from {signal_text}, with strongest emphasis on {rationale_map[variant]}."


def infer_custom_theme(
    spec: SiteSpec,
    documents: list[SourceDocument],
    passages: list[RetrievedPassage],
) -> ThemeSpec:
    variant = select_style_family(spec, documents, passages)
    preset = THEME_PRESETS[variant]

    return ThemeSpec(
        name=preset["name"],
        rationale=build_rationale(variant, spec, documents),
        font_family=preset["font_family"],
        background=preset["background"],
        ink=preset["ink"],
        muted=preset["muted"],
        card=preset["card"],
        accent=preset["accent"],
        accent_soft=preset["accent_soft"],
        border=preset["border"],
        cover_gradient=preset["cover_gradient"],
        variant=variant,
    )
