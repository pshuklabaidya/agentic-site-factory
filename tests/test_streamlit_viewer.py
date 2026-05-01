from pathlib import Path


def test_generated_site_viewer_uses_st_html_with_javascript_helper():
    app = Path("app/Home.py").read_text(encoding="utf-8")

    assert "import streamlit.components.v1 as components" not in app
    assert "components.html" not in app
    assert "def render_generated_html" in app
    assert "unsafe_allow_javascript=True" in app
    assert "render_generated_html(page_html)" in app
    assert "render_generated_html(preview_html)" in app


def test_generated_site_viewer_rewrites_links_before_rendering():
    app = Path("app/Home.py").read_text(encoding="utf-8")

    assert "rewrite_generated_site_links_for_viewer(page_html, generated_site_slug)" in app
    assert "rewrite_generated_site_links_for_viewer(result.site.html, site_slug)" in app
