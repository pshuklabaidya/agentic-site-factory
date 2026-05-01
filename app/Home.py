from __future__ import annotations

from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components

from agentic_site_factory.agents import generate_sections, openai_available, plan_site
from agentic_site_factory.artifacts import save_artifact_bundle
from agentic_site_factory.ingestion import extract_uploaded_document, load_local_text_documents
from agentic_site_factory.models import SiteSpec, SourceDocument
from agentic_site_factory.quality import evaluate_site
from agentic_site_factory.retrieval import retrieve_passages
from agentic_site_factory.site_builder import build_html


ROOT = Path(__file__).resolve().parents[1]

st.set_page_config(
    page_title="Agentic Site Factory",
    page_icon="ASF",
    layout="wide",
)

st.title("Agentic Site Factory")
st.caption("Agentic RAG website builder for authors, creators, and small businesses.")

with st.sidebar:
    st.header("Website Specification")
    author_name = st.text_input("Author or brand name", value="Elena Vale")
    audience = st.text_input("Audience", value="literary fiction readers and book clubs")
    tone = st.text_input("Tone", value="warm, elegant, and immersive")
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
    requested_sections=requested_sections,
)

query = f"{author_name} {audience} {website_goal} {' '.join(requested_sections)}"
passages = retrieve_passages(documents, query=query, top_k=6)

left, right = st.columns([0.44, 0.56])

with left:
    st.subheader("Agent Plan")

    if documents and requested_sections:
        plan = plan_site(spec, passages)
        st.write(f"**Title:** {plan.title}")
        st.write(f"**Sections:** {', '.join(plan.sections)}")
        st.write(plan.content_strategy)
        generation_mode = "OpenAI API" if openai_available() else "Deterministic local fallback"
        st.write(f"**Generation mode:** {generation_mode}")
        st.write("**Agent workflow:**")

        for step in plan.agent_steps:
            st.write(f"- {step}")
    else:
        plan = None
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
        current_plan = plan_site(spec, passages)
        sections = generate_sections(spec, passages)
        site = build_html(spec, sections)
        quality_report = evaluate_site(spec, site, passages)
        output_dir = ROOT / "generated_sites" / "latest"
        manifest = save_artifact_bundle(
            output_dir=output_dir,
            spec=spec,
            plan=current_plan,
            site=site,
            passages=passages,
            quality_report=quality_report,
        )

        st.success(f"Website generated in {output_dir}")
        st.write(f"**Quality passed:** {quality_report.passed}")
        st.write(f"**Artifact files:** {', '.join(manifest.files)}")

        with st.expander("Quality Report"):
            for check in quality_report.checks:
                icon = "PASS" if check.passed else "FAIL"
                st.write(f"**{icon} - {check.name}:** {check.detail}")

        st.download_button(
            "Download index.html",
            data=site.html,
            file_name="index.html",
            mime="text/html",
        )
        components.html(site.html, height=760, scrolling=True)
    else:
        st.write("Click Build Website to generate the static site.")
