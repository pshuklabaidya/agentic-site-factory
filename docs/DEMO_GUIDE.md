# Demo Guide

Agentic Site Factory can be demonstrated in two ways: through the Streamlit dashboard or through the command-line demo generator.

## Streamlit Demo

Run the app from the repository root.

    source .venv/bin/activate
    streamlit run app/Home.py

Recommended demo flow:

1. Keep the synthetic sample manuscript enabled.
2. Review the default website specification.
3. Click Build Website.
4. Review the agent plan and retrieved evidence.
5. Inspect the generated website preview.
6. Download index.html.
7. Confirm generated_sites/latest contains the artifact bundle.

Generated files:

- index.html
- site_plan.json
- evidence_map.json
- quality_report.json
- artifact_manifest.json

## Command-Line Demo

Run the deterministic demo generator from the repository root.

    source .venv/bin/activate
    python scripts/generate_demo_site.py

The command writes a demo artifact bundle to:

    generated_sites/demo_cli

This is useful for quick verification without launching the dashboard.

## Optional OpenAI Demo

Set environment variables before launching the app.

    export OPENAI_API_KEY="your-key-here"
    export OPENAI_MODEL="gpt-5-mini"

Without an API key, the deterministic local fallback remains fully functional.


- Custom style-aware website rendering with literary, modern, and dark styles.


- Full artifact bundle download as a ZIP file.


- Custom aesthetics are inferred from the website specification, optional style guidance, retrieved passages, and uploaded source material.


- The generated artifact bundle includes theme_spec.json with the inferred visual style rationale and CSS values.


- OpenAI configuration supports environment variables, local .env files, and Streamlit secrets.

## OpenAI Runtime Behavior

The Streamlit app uses OpenAI generation when `OPENAI_API_KEY` is available. Repository validation commands use deterministic local generation by setting `AGENTIC_SITE_FACTORY_DISABLE_OPENAI=1`, so tests and CLI demos stay fast and do not spend API credits.

