from __future__ import annotations

from io import BytesIO
from pathlib import Path

from pypdf import PdfReader

from agentic_site_factory.models import SourceDocument


def clean_text(text: str) -> str:
    return " ".join(text.replace("\x00", " ").split())


def extract_text_from_txt_bytes(data: bytes) -> str:
    return clean_text(data.decode("utf-8", errors="ignore"))


def extract_text_from_pdf_bytes(data: bytes) -> str:
    reader = PdfReader(BytesIO(data))
    page_text: list[str] = []

    for page in reader.pages:
        page_text.append(page.extract_text() or "")

    return clean_text("\n".join(page_text))


def extract_uploaded_document(filename: str, data: bytes) -> SourceDocument:
    suffix = Path(filename).suffix.lower()

    if suffix == ".pdf":
        text = extract_text_from_pdf_bytes(data)
    elif suffix == ".txt":
        text = extract_text_from_txt_bytes(data)
    else:
        raise ValueError(f"Unsupported file type: {suffix}")

    return SourceDocument(name=filename, text=text)


def load_local_text_documents(paths: list[Path]) -> list[SourceDocument]:
    documents: list[SourceDocument] = []

    for path in paths:
        if path.exists() and path.is_file():
            documents.append(
                SourceDocument(
                    name=path.name,
                    text=extract_text_from_txt_bytes(path.read_bytes()),
                )
            )

    return documents
