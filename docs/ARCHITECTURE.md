# Architecture

Agentic Site Factory is organized around a shared generation pipeline that can be called from Streamlit or from command-line scripts.

## System Flow

    User specification
          |
          v
    Intake agent
          |
          v
    Document ingestion
          |
          v
    Retrieval agent
          |
          v
    Planner agent
          |
          v
    Writer agent
          |
          v
    Builder agent
          |
          v
    Quality agent
          |
          v
    Artifact agent
          |
          v
    Static website bundle

## Main Components

### Streamlit Dashboard

File:

    app/Home.py

Responsibilities:

- Captures author and website specification.
- Accepts TXT and PDF uploads.
- Shows retrieved evidence.
- Displays agent plan.
- Builds and previews the website.
- Downloads index.html and the full artifact ZIP.

### Shared Pipeline

File:

    src/agentic_site_factory/pipeline.py

Responsibilities:

- Builds the retrieval query.
- Retrieves evidence.
- Creates the site plan.
- Generates sections.
- Builds HTML.
- Runs quality checks.
- Saves the artifact bundle.

### Ingestion

File:

    src/agentic_site_factory/ingestion.py

Responsibilities:

- Extracts text from TXT files.
- Extracts text from PDF files.
- Cleans document text.
- Converts source material into structured SourceDocument objects.

### Retrieval

File:

    src/agentic_site_factory/retrieval.py

Responsibilities:

- Splits documents into chunks.
- Builds TF-IDF vectors.
- Scores source chunks against the website specification.
- Returns ranked retrieved passages.

### Agents

File:

    src/agentic_site_factory/agents.py

Responsibilities:

- Plans the website.
- Generates section copy.
- Uses deterministic fallback generation by default.
- Optionally uses the OpenAI API when OPENAI_API_KEY is available.

### Site Builder

File:

    src/agentic_site_factory/site_builder.py

Responsibilities:

- Renders custom style-aware HTML.
- Supports custom inferred visual styles.
- Includes demo commerce behavior.
- Produces a standalone static site.

### Quality Layer

File:

    src/agentic_site_factory/quality.py

Responsibilities:

- Checks requested section coverage.
- Checks retrieved evidence availability.
- Checks source attribution.
- Checks HTML structure.
- Checks demo commerce behavior.

### Artifact Layer

Files:

    src/agentic_site_factory/artifacts.py
    src/agentic_site_factory/bundle.py

Responsibilities:

- Writes index.html.
- Writes site_plan.json.
- Writes evidence_map.json.
- Writes quality_report.json.
- Writes artifact_manifest.json.
- Creates a ZIP archive of the generated bundle.

## Command-Line Entry Points

Generate the default demo:

    python scripts/generate_demo_site.py

Generate from JSON specification:

    python scripts/generate_from_spec.py --spec data/sample_specs/elena_vale_author_site.json

## Design Principles

- Deterministic local mode remains available without paid API usage.
- Optional OpenAI generation improves copy quality when credentials are present.
- All generated claims should be grounded in retrieved source material.
- Generated artifacts are ignored by Git.
- Tests cover the retrieval, ingestion, pipeline, quality, artifact, theme, and bundle layers.


- Custom aesthetics are inferred from the website specification, optional style guidance, retrieved passages, and uploaded source material.


- The generated artifact bundle includes theme_spec.json with the inferred visual style rationale and CSS values.


- Generated sites are published to Streamlit static files and opened as real separate-tab pages.


- Streamlit static serving is enabled so generated sites open as real separate-tab pages under `/app/static/...`.
