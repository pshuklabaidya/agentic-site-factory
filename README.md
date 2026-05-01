# Agentic Site Factory

![CI](https://github.com/pshuklabaidya/agentic-site-factory/actions/workflows/ci.yml/badge.svg)


Agentic Site Factory is an Agentic RAG portfolio project that turns uploaded manuscripts and natural-language website specifications into generated static website artifacts through an interactive Streamlit dashboard.

## Status

Portfolio-ready baseline complete.

Core application, shared pipeline, CLI demo, JSON spec generation, quality checks, artifact bundling, tests, linting, CI, and documentation are in place.

## Purpose

The project demonstrates how an agentic workflow can transform source documents into a working website package. A user can upload manuscript-like material, describe the desired site, and receive a generated author website with grounded page copy and downloadable artifacts.

## Core Workflow

1. Intake agent normalizes the website specification.
2. Retrieval agent selects source-grounded passages from uploaded material.
3. Planner agent maps requested sections to page responsibilities.
4. Writer agent creates section copy from retrieved evidence.
5. Builder agent renders a static website.
6. Quality agent checks coverage, evidence, HTML structure, and demo commerce behavior.
7. Artifact agent saves the generated site package.

## Features

- Streamlit static serving is enabled so generated sites open as real separate-tab pages under `/app/static/...`.

- Generated sites are published to Streamlit static files and opened as real separate-tab pages.

- OpenAI configuration supports environment variables, local .env files, and Streamlit secrets.

- The generated artifact bundle includes theme_spec.json with the inferred visual style rationale and CSS values.

- Custom aesthetics are inferred from the website specification, optional style guidance, retrieved passages, and uploaded source material.

- Full artifact bundle download as a ZIP file.

- Custom style-aware website rendering with literary, modern, and dark styles.

- Upload TXT and PDF source material.
- Retrieve relevant passages from uploaded documents.
- Generate a website plan from a user specification.
- Produce grounded content for website sections.
- Render a static HTML website artifact.
- Preview and download the generated site from Streamlit.
- Save a site plan, evidence map, quality report, and artifact manifest.
- Run with deterministic local fallback logic.
- Optionally use the OpenAI API for richer generation.
- Validate the repository with Pytest, Ruff, and GitHub Actions CI.

## Repository Structure

- app/Home.py - Streamlit dashboard.
- src/agentic_site_factory/agents.py - Planner and writer agent logic.
- src/agentic_site_factory/artifacts.py - Artifact bundle generation.
- src/agentic_site_factory/ingestion.py - TXT and PDF extraction.
- src/agentic_site_factory/models.py - Pydantic data models.
- src/agentic_site_factory/quality.py - Deterministic quality checks.
- src/agentic_site_factory/retrieval.py - TF-IDF retrieval.
- src/agentic_site_factory/site_builder.py - Static HTML renderer.
- src/agentic_site_factory/pipeline.py - Shared generation pipeline.
- data/sample_manuscripts/ - Synthetic sample content.
- generated_sites/ - Generated website output.
- tests/ - Unit tests.
- docs/PORTFOLIO_OVERVIEW.md - Portfolio explanation.
- docs/DEMO_GUIDE.md - Demo walkthrough.
- docs/DEPLOYMENT.md - Local, Codespaces, and Streamlit deployment notes.
- docs/ARCHITECTURE.md - System architecture and component responsibilities.
- docs/ROADMAP.md - Completed baseline and future enhancements.

## Developer Commands

Common commands are available through Make.

    make install
    make test
    make lint
    make check
    make demo
    make app
    make clean

## Local Setup

Run the following commands from the repository root.

    python -m venv .venv
    source .venv/bin/activate
    pip install -e ".[dev]"
    pytest
    ruff check .
    streamlit run app/Home.py

## OpenAI Runtime Behavior

The Streamlit app uses OpenAI generation when `OPENAI_API_KEY` is available. Repository validation commands use deterministic local generation by setting `AGENTIC_SITE_FACTORY_DISABLE_OPENAI=1`, so tests and CLI demos stay fast and do not spend API credits.

## Optional OpenAI Usage

Set these environment variables before running Streamlit.

    export OPENAI_API_KEY="your-key-here"
    export OPENAI_MODEL="gpt-5-mini"

Without an API key, deterministic local fallback mode remains fully functional.

## JSON Specification Demo

Generate a website from a JSON specification.

    source .venv/bin/activate
    python scripts/generate_from_spec.py --spec data/sample_specs/elena_vale_author_site.json

The command writes output to:

    generated_sites/spec_demo

## Command-Line Demo

Generate a demo artifact bundle without launching Streamlit.

    source .venv/bin/activate
    python scripts/generate_demo_site.py

The command writes output to:

    generated_sites/demo_cli

See docs/DEMO_GUIDE.md for the full walkthrough.

## Generated Output

After clicking Build Website in the app, the generated artifact bundle is saved to:

    generated_sites/latest

The bundle contains:

- index.html
- site_plan.json
- evidence_map.json
- quality_report.json
- artifact_manifest.json

## Portfolio Disclosure

This repository uses synthetic sample content for demonstration purposes. Uploaded local files remain part of the local app session and are not committed by default.
