from pathlib import Path
from zipfile import ZipFile

from agentic_site_factory.bundle import create_zip_archive


def test_create_zip_archive_writes_source_files(tmp_path: Path):
    source_dir = tmp_path / "site"
    source_dir.mkdir()
    (source_dir / "index.html").write_text("<html></html>", encoding="utf-8")
    (source_dir / "quality_report.json").write_text("{}", encoding="utf-8")

    archive_path = create_zip_archive(source_dir, tmp_path / "bundle.zip")

    assert archive_path.exists()

    with ZipFile(archive_path) as zip_file:
        names = set(zip_file.namelist())

    assert names == {"index.html", "quality_report.json"}
