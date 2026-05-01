from __future__ import annotations

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from agentic_site_factory.models import RetrievedPassage, SourceDocument


def chunk_text(text: str, chunk_size: int = 900, overlap: int = 150) -> list[str]:
    cleaned = " ".join(text.split())
    if not cleaned:
        return []

    chunks: list[str] = []
    start = 0

    while start < len(cleaned):
        end = start + chunk_size
        chunks.append(cleaned[start:end])

        if end >= len(cleaned):
            break

        start = max(0, end - overlap)

    return chunks


def retrieve_passages(
    documents: list[SourceDocument],
    query: str,
    top_k: int = 5,
) -> list[RetrievedPassage]:
    passages: list[tuple[str, str]] = []

    for document in documents:
        for chunk in chunk_text(document.text):
            passages.append((document.name, chunk))

    if not passages:
        return []

    corpus = [text for _, text in passages]
    vectorizer = TfidfVectorizer(stop_words="english")

    matrix = vectorizer.fit_transform(corpus)
    query_vector = vectorizer.transform([query])
    scores = cosine_similarity(query_vector, matrix).flatten()

    ranked_indices = scores.argsort()[::-1][:top_k]

    return [
        RetrievedPassage(
            source=passages[index][0],
            text=passages[index][1],
            score=float(scores[index]),
        )
        for index in ranked_indices
    ]
