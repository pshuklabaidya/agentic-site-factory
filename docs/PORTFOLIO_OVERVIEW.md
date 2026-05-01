# Portfolio Overview

Agentic Site Factory demonstrates an Agentic RAG workflow that turns manuscript-like source material and a natural-language website specification into a generated static website artifact.

## Problem

Authors, creators, and small businesses often have source material but lack a fast way to turn that material into a polished web presence. Generic website builders require manual writing, manual structuring, and manual content transfer.

## Solution

The application uses a simple agentic workflow:

1. Intake agent captures the desired website specification.
2. Retrieval agent selects relevant evidence from uploaded source material.
3. Planner agent maps the specification into website sections.
4. Writer agent generates grounded section copy.
5. Builder agent renders a static HTML website.
6. Quality agent checks section coverage, evidence use, HTML structure, and demo commerce behavior.
7. Artifact agent writes the generated site package and supporting JSON files.

## Current Features

- Streamlit dashboard.
- TXT and PDF document upload.
- TF-IDF retrieval over source document chunks.
- Deterministic fallback generation.
- Optional OpenAI-powered section generation.
- Static HTML website preview.
- Downloadable index.html artifact.
- Artifact manifest output.
- Evidence map output.
- Quality report output.
- Pytest and Ruff coverage.
- GitHub Actions CI.

## Generated Artifacts

The app writes the following files to generated_sites/latest after a website build:

- index.html
- site_plan.json
- evidence_map.json
- quality_report.json
- artifact_manifest.json

## Technical Stack

- Python
- Streamlit
- Pydantic
- scikit-learn
- pypdf
- OpenAI API optional
- Pytest
- Ruff
- GitHub Actions

## Portfolio Value

This project shows practical ability across:

- Agentic AI system design
- RAG-style retrieval
- Document ingestion
- LLM application architecture
- Structured outputs
- Testable AI workflows
- Streamlit dashboard development
- Static artifact generation
- AI portfolio packaging
