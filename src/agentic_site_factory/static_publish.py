from __future__ import annotations

import re
import shutil
from html import escape
from pathlib import Path


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", value.strip().lower())
    slug = slug.strip("-")
    return slug or "generated-site"


def publish_static_site(
    source_dir: Path,
    static_root: Path,
    site_name: str,
) -> tuple[Path, str]:
    site_slug = slugify(site_name)
    destination = static_root / "generated_sites" / site_slug

    if destination.exists():
        shutil.rmtree(destination)

    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(source_dir, destination)

    return destination, site_slug


def page_name_from_filename(filename: str) -> str:
    safe = slugify(filename.removesuffix(".html"))

    if safe == "index":
        return "index"

    return safe


def page_filename_from_name(page_name: str) -> str:
    safe = page_name_from_filename(page_name)

    if safe == "index":
        return "index.html"

    return f"{safe}.html"


def generated_site_viewer_url(site_slug: str, page_name: str = "index") -> str:
    safe_slug = slugify(site_slug)
    safe_page = page_name_from_filename(page_name)
    return f"?generated_site={safe_slug}&page={safe_page}"


def generated_site_page_path(
    static_root: Path,
    site_slug: str,
    page_name: str = "index",
) -> Path:
    safe_slug = slugify(site_slug)
    filename = page_filename_from_name(page_name)
    return static_root / "generated_sites" / safe_slug / filename


def generated_site_index_path(static_root: Path, site_slug: str) -> Path:
    return generated_site_page_path(static_root, site_slug, "index")


def rewrite_generated_site_links_for_viewer(html: str, site_slug: str) -> str:
    safe_slug = slugify(site_slug)

    def replace_href(match: re.Match[str]) -> str:
        quote = match.group(1)
        filename = match.group(2)
        page_name = page_name_from_filename(filename)
        href = generated_site_viewer_url(safe_slug, page_name)
        return f'href={quote}{escape(href)}{quote} target="_top"'

    return re.sub(r'href=(["\'])([A-Za-z0-9_-]+\.html)\1', replace_href, html)


def create_static_site_link(
    site_slug: str,
    label: str = "Open generated website in new tab",
) -> str:
    href = generated_site_viewer_url(site_slug, "index")
    return (
        f'<a href="{escape(href)}" target="_blank" rel="noopener noreferrer" '
        'style="display:inline-block;padding:0.75rem 1rem;border-radius:999px;'
        'background:#6d28d9;color:white;font-weight:700;text-decoration:none;">'
        f"{escape(label)}</a>"
    )
