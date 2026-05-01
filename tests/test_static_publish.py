from pathlib import Path

from agentic_site_factory.static_publish import (
    create_static_site_link,
    publish_static_site,
    slugify,
)


def test_slugify_creates_safe_slug():
    assert slugify("Elena Vale!") == "elena-vale"


def test_publish_static_site_copies_files_and_returns_url(tmp_path: Path):
    source_dir = tmp_path / "source"
    static_root = tmp_path / "static"
    source_dir.mkdir()
    (source_dir / "index.html").write_text("<html></html>", encoding="utf-8")

    destination, url = publish_static_site(
        source_dir=source_dir,
        static_root=static_root,
        site_name="Elena Vale",
    )

    assert (destination / "index.html").exists()
    assert url == "/app/static/generated_sites/elena-vale/index.html"


def test_create_static_site_link_opens_new_tab():
    link = create_static_site_link("/app/static/generated_sites/elena-vale/index.html")

    assert 'target="_blank"' in link
    assert 'rel="noopener noreferrer"' in link
    assert "Open generated website in new tab" in link
