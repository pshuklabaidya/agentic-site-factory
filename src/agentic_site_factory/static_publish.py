from __future__ import annotations

import re
import shutil
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

    return destination, f"/app/static/generated_sites/{site_slug}/index.html"
