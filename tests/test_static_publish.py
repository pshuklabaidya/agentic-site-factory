from pathlib import Path

from agentic_site_factory.static_publish import (
    create_static_site_link,
    generated_site_index_path,
    generated_site_page_path,
    generated_site_viewer_url,
    publish_static_site,
    rewrite_generated_site_links_for_viewer,
    slugify,
)


def test_slugify_creates_safe_slug():
    assert slugify("Elena Vale!") == "elena-vale"


def test_publish_static_site_copies_files_and_returns_slug(tmp_path: Path):
    source_dir = tmp_path / "source"
    static_root = tmp_path / "static"
    source_dir.mkdir()
    (source_dir / "index.html").write_text("<html></html>", encoding="utf-8")
    (source_dir / "books.html").write_text("<html></html>", encoding="utf-8")

    destination, slug = publish_static_site(
        source_dir=source_dir,
        static_root=static_root,
        site_name="Elena Vale",
    )

    assert (destination / "index.html").exists()
    assert (destination / "books.html").exists()
    assert slug == "elena-vale"


def test_generated_site_viewer_url_uses_query_param():
    assert generated_site_viewer_url("elena-vale") == "?generated_site=elena-vale&page=index"
    assert generated_site_viewer_url("elena-vale", "books") == "?generated_site=elena-vale&page=books"


def test_generated_site_index_path_points_to_html_file(tmp_path: Path):
    path = generated_site_index_path(tmp_path / "static", "Elena Vale")

    assert path.as_posix().endswith("static/generated_sites/elena-vale/index.html")


def test_generated_site_page_path_points_to_requested_page(tmp_path: Path):
    path = generated_site_page_path(tmp_path / "static", "Elena Vale", "books")

    assert path.as_posix().endswith("static/generated_sites/elena-vale/books.html")


def test_create_static_site_link_opens_new_tab():
    link = create_static_site_link("elena-vale")

    assert 'href="?generated_site=elena-vale&amp;page=index"' in link
    assert 'target="_blank"' in link
    assert 'rel="noopener noreferrer"' in link
    assert "Open generated website in new tab" in link


def test_rewrite_generated_site_links_for_viewer_rewrites_html_pages():
    html = '<nav><a href="index.html">Home</a><a href="books.html">Books</a></nav>'

    rewritten = rewrite_generated_site_links_for_viewer(html, "elena-vale")

    assert 'href="?generated_site=elena-vale&amp;page=index" target="_top"' in rewritten
    assert 'href="?generated_site=elena-vale&amp;page=books" target="_top"' in rewritten
