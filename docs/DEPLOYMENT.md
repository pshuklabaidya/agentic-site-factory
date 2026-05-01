# Deployment Guide

## Streamlit Community Cloud

Use these settings:

    Repository: pshuklabaidya/agentic-site-factory
    Branch: main
    Main file path: app/Home.py

The repository includes requirements.txt with `-e .` so the package under `src/` is installed before the Streamlit app starts.

Secrets:

    OPENAI_API_KEY = "your-openai-api-key"
    OPENAI_MODEL = "gpt-5-mini"

The app also works without secrets through deterministic fallback generation.

## Local or Codespaces Run

    python -m venv .venv
    source .venv/bin/activate
    make install
    make check
    make app

## Static Generated-Site Links

Static serving is enabled in .streamlit/config.toml. Generated websites are copied under:

    app/static/generated_sites/

The app exposes generated sites through URLs like:

    /app/static/generated_sites/site-name/index.html

These generated runtime files are useful during the active app session. They are not intended as permanent storage.



- Generated websites are multi-page static artifacts with index.html plus one HTML file per generated section.


- The Books page lists uploaded documents classified as books, with brief summaries.


- Each detected book gets its own generated book page with an Add to Cart action.


- The demo cart uses browser localStorage so cart contents persist across generated pages and browser sessions.
