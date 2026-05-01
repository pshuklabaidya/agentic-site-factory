from agentic_site_factory.models import SourceDocument
from agentic_site_factory.retrieval import chunk_text, retrieve_passages


def test_chunk_text_returns_chunks():
    chunks = chunk_text("alpha beta gamma", chunk_size=10, overlap=2)

    assert chunks
    assert chunks[0].startswith("alpha")


def test_retrieve_passages_returns_relevant_result():
    documents = [
        SourceDocument(
            name="book.txt",
            text="This novel is about coastal memory, family secrets, and reconciliation.",
        ),
        SourceDocument(
            name="manual.txt",
            text="A technical manual about database indexing and query planning.",
        ),
    ]

    results = retrieve_passages(documents, query="family memory novel", top_k=1)

    assert len(results) == 1
    assert results[0].source == "book.txt"
