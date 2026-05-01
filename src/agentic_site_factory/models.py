from __future__ import annotations

from pydantic import BaseModel, Field


class SiteSpec(BaseModel):
    author_name: str = Field(default="Demo Author")
    audience: str = Field(default="general readers")
    tone: str = Field(default="warm, professional, literary")
    website_goal: str = Field(default="promote books and invite readers to learn more")
    style_guidance: str = Field(
        default="",
        description="Optional visual style guidance. Leave blank for inferred styling.",
    )
    requested_sections: list[str] = Field(
        default_factory=lambda: ["hero", "bio", "books", "gallery", "shop", "contact"]
    )


class SourceDocument(BaseModel):
    name: str
    text: str


class RetrievedPassage(BaseModel):
    source: str
    text: str
    score: float


class SitePlan(BaseModel):
    title: str
    sections: list[str]
    content_strategy: str
    agent_steps: list[str]


class GeneratedSection(BaseModel):
    name: str
    heading: str
    body: str
    evidence_sources: list[str] = Field(default_factory=list)


class ThemeSpec(BaseModel):
    name: str
    rationale: str
    font_family: str
    background: str
    ink: str
    muted: str
    card: str
    accent: str
    accent_soft: str
    border: str
    cover_gradient: str


class GeneratedSite(BaseModel):
    title: str
    html: str
    sections: list[GeneratedSection]
    theme: ThemeSpec
    pages: dict[str, str] = Field(default_factory=dict)
