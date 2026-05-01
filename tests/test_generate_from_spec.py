from pathlib import Path

from agentic_site_factory.spec_generation import build_site_from_spec_file, load_generation_spec


def test_load_generation_spec_reads_sample_spec():
    spec_path = Path("data/sample_specs/elena_vale_author_site.json")

    spec = load_generation_spec(spec_path)

    assert spec.author_name == "Elena Vale"
    assert spec.style_guidance == ""
    assert "shop" in spec.requested_sections
    assert spec.source_files == ["data/sample_manuscripts/elena_vale.txt"]


def test_build_site_from_spec_file_generates_artifacts(tmp_path):
    manuscript_path = tmp_path / "sample.txt"
    manuscript_path.write_text(
        "Elena Vale writes literary fiction about memory, books, readers, and family stories.",
        encoding="utf-8",
    )

    spec_path = tmp_path / "spec.json"
    spec_path.write_text(
        """
{
  "author_name": "Elena Vale",
  "audience": "readers",
  "tone": "warm",
  "website_goal": "Introduce books to readers.",
  "style_guidance": "modern professional",
  "requested_sections": ["hero", "shop"],
  "source_files": ["sample.txt"],
  "output_dir": "output"
}
""".strip(),
        encoding="utf-8",
    )

    output_dir = build_site_from_spec_file(spec_path=spec_path, root=tmp_path)

    assert (output_dir / "index.html").exists()
    assert (output_dir / "artifact_manifest.json").exists()
    assert (output_dir / "theme_spec.json").exists()
