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
    OPENAI_MODEL="gpt-4o-mini"

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
