from __future__ import annotations

from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components

from agentic_site_factory.agents import openai_available, plan_site
from agentic_site_factory.bundle import create_zip_archive
from agentic_site_factory.ingestion import extract_uploaded_document, load_local_text_documents
from agentic_site_factory.models import SiteSpec, SourceDocument
from agentic_site_factory.pipeline import run_generation_pipeline
from agentic_site_factory.preview_links import create_open_site_link
from agentic_site_factory.retrieval import retrieve_passages
from agentic_site_factory.theming import infer_custom_theme


ROOT = Path(__file__).resolve().parents[1]

st.set_page_config(
    page_title="Agentic Site Factory",
    page_icon=":building_construction:",
    layout="wide",
)

st.title("Agentic Site Factory")
st.caption("Agentic RAG website builder for authors, creators, and small businesses.")

with st.sidebar:
    st.header("Website Specification")
    author_name = st.text_input("Author or brand name", value="Elena Vale")
    audience = st.text_input("Audience", value="literary fiction readers and book clubs")
    tone = st.text_input("Tone", value="warm, elegant, and immersive")
    style_guidance = st.text_area(
        "Optional style guidance",
        value="",
        placeholder=(
            "Leave blank to infer custom aesthetics from the specification and uploaded files."
        ),
    )
    website_goal = st.text_area(
        "Website goal",
        value=(
            "Introduce the author, showcase books, and help readers explore and purchase "
            "featured titles."
        ),
    )
    requested_sections = st.multiselect(
        "Sections",
        ["hero", "bio", "books", "gallery", "shop", "contact"],
        default=["hero", "bio", "books", "gallery", "shop", "contact"],
    )

st.subheader("Source Material")
uploaded_files = st.file_uploader(
    "Upload manuscript or notes as TXT or PDF files",
    type=["txt", "pdf"],
    accept_multiple_files=True,
)

use_sample = st.checkbox("Use synthetic sample manuscript text", value=True)

documents: list[SourceDocument] = []

if use_sample:
    sample_paths = [ROOT / "data" / "sample_manuscripts" / "elena_vale.txt"]
    documents.extend(load_local_text_documents(sample_paths))

if uploaded_files:
    for uploaded_file in uploaded_files:
        try:
            documents.append(extract_uploaded_document(uploaded_file.name, uploaded_file.getvalue()))
        except ValueError as exc:
            st.warning(str(exc))

spec = SiteSpec(
    author_name=author_name,
    audience=audience,
    tone=tone,
    website_goal=website_goal,
    style_guidance=style_guidance,
    requested_sections=requested_sections,
)

preview_query = " ".join(
    [
        spec.author_name,
        spec.audience,
        spec.tone,
        spec.website_goal,
        spec.style_guidance,
        " ".join(spec.requested_sections),
    ]
)
passages = retrieve_passages(documents, query=preview_query, top_k=6)
preview_theme = infer_custom_theme(spec, documents, passages)

left, right = st.columns([0.44, 0.56])

with left:
    st.subheader("Agent Plan")

    if documents and requested_sections:
        preview_plan = plan_site(spec, passages)
        st.write(f"**Title:** {preview_plan.title}")
        st.write(f"**Sections:** {', '.join(preview_plan.sections)}")
        st.write(f"**Inferred visual style:** {preview_theme.name}")
        st.write(f"**Style rationale:** {preview_theme.rationale}")
        st.write(preview_plan.content_strategy)
        generation_mode = "OpenAI API" if openai_available() else "Deterministic local fallback"
        st.write(f"**Generation mode:** {generation_mode}")
        st.write("**Agent workflow:**")

        for step in preview_plan.agent_steps:
            st.write(f"- {step}")
    else:
        st.info("Add source material and choose at least one section.")

    st.subheader("Retrieved Evidence")

    if passages:
        for passage in passages[:4]:
            st.markdown(f"**{passage.source}** - score {passage.score:.3f}")
            preview = passage.text[:500] + ("..." if len(passage.text) > 500 else "")
            st.write(preview)
    else:
        st.write("No retrieved passages yet.")

with right:
    st.subheader("Generated Website")
    disabled = not documents or not requested_sections

    if st.button("Build Website", type="primary", disabled=disabled):
        output_dir = ROOT / "generated_sites" / "latest"
        zip_path = ROOT / "generated_sites" / "latest_site_bundle.zip"
        result = run_generation_pipeline(
            spec=spec,
            documents=documents,
            output_dir=output_dir,
            top_k=6,
        )
        create_zip_archive(output_dir, zip_path)

        st.success(f"Website generated in {output_dir}")
        st.write(f"**Inferred visual style:** {result.site.theme.name}")
        st.write(f"**Style rationale:** {result.site.theme.rationale}")
        st.write(f"**Quality passed:** {result.quality_report.passed}")

        if result.manifest is not None:
            st.write(f"**Artifact files:** {', '.join(result.manifest.files)}")

        st.markdown(create_open_site_link(result.site.html), unsafe_allow_html=True)

        with st.expander("Quality Report"):
            for check in result.quality_report.checks:
                icon = "PASS" if check.passed else "FAIL"
                st.write(f"**{icon} - {check.name}:** {check.detail}")

        st.download_button(
            "Download index.html",
            data=result.site.html,
            file_name="index.html",
            mime="text/html",
        )
        st.download_button(
            "Download full artifact bundle",
            data=zip_path.read_bytes(),
            file_name="agentic_site_factory_bundle.zip",
            mime="application/zip",
        )
        components.html(result.site.html, height=760, scrolling=True)
    else:
        st.write("Click Build Website to generate the static site.")
