from __future__ import annotations

import argparse
from pathlib import Path

from agentic_site_factory.spec_generation import build_site_from_spec_file


ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate a site from a JSON specification.")
    parser.add_argument(
        "--spec",
        default="data/sample_specs/elena_vale_author_site.json",
        help="Path to the JSON generation specification.",
    )
    args = parser.parse_args()

    output_dir = build_site_from_spec_file(
        spec_path=(ROOT / args.spec).resolve(),
        root=ROOT,
    )
    print(f"Site generated at: {output_dir}")
    print(f"Open this file: {output_dir / 'index.html'}")


if __name__ == "__main__":
    main()
