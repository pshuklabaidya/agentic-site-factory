# Deployment Guide

Agentic Site Factory can run locally, in GitHub Codespaces, or on Streamlit Community Cloud.

## Local or Codespaces Run

From the repository root:

    python -m venv .venv
    source .venv/bin/activate
    make install
    make check
    make app

The Streamlit app starts from:

    app/Home.py

## Streamlit Community Cloud

Recommended settings:

- Main file path: app/Home.py
- Python version: 3.12
- Package install command: pip install -e ".[dev]"

Optional secrets:

    OPENAI_API_KEY="your-key-here"
    OPENAI_MODEL="gpt-5-mini"

The app runs without secrets through deterministic local fallback mode.

## GitHub Codespaces

Recommended flow:

    source .venv/bin/activate
    make check
    make app

When Streamlit starts, Codespaces will expose a forwarded port. Open the forwarded port in a browser.

## Command-Line Artifact Demo

The static artifact pipeline can run without the dashboard:

    source .venv/bin/activate
    make demo

Output location:

    generated_sites/demo_cli

## Generated Artifacts

Generated website bundles are intentionally ignored by Git. The repository keeps only:

    generated_sites/.gitkeep

This prevents local uploads and generated files from being accidentally committed.


- Custom aesthetics are inferred from the website specification, optional style guidance, retrieved passages, and uploaded source material.


- The generated artifact bundle includes theme_spec.json with the inferred visual style rationale and CSS values.


- OpenAI configuration supports environment variables, local .env files, and Streamlit secrets.

## OpenAI Runtime Behavior

The Streamlit app uses OpenAI generation when `OPENAI_API_KEY` is available. Repository validation commands use deterministic local generation by setting `AGENTIC_SITE_FACTORY_DISABLE_OPENAI=1`, so tests and CLI demos stay fast and do not spend API credits.



- Generated sites are published to Streamlit static files and opened as real separate-tab pages.


- Streamlit static serving is enabled so generated sites open as real separate-tab pages under `/app/static/...`.
