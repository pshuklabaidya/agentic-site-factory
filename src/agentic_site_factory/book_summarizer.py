from __future__ import annotations

import re

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from agentic_site_factory.text_sanitizer import sanitize_body


def split_sentences(text: str) -> list[str]:
    cleaned = sanitize_body(text)
    if not cleaned:
        return []

    sentences = re.split(r"(?<=[.!?])\s+", cleaned)
    return [sentence.strip() for sentence in sentences if len(sentence.strip()) > 25]


def summarize_book_text(text: str, max_sentences: int = 4) -> str:
    sentences = split_sentences(text)

    if not sentences:
        return "Summary unavailable from the supplied text."

    if len(sentences) <= max_sentences:
        return " ".join(sentences)

    matrix = TfidfVectorizer(stop_words="english").fit_transform(sentences)
    centroid = np.asarray(matrix.mean(axis=0)).reshape(1, -1)
    similarity = cosine_similarity(matrix, centroid).ravel()

    position_bonus = np.linspace(0.12, 0.03, len(sentences))
    ending_bonus = np.linspace(0.02, 0.10, len(sentences))
    scores = similarity + position_bonus + ending_bonus

    ranked = list(np.argsort(scores)[::-1])
    selected: set[int] = set()

    first_band = range(0, max(1, len(sentences) // 3))
    middle_band = range(max(1, len(sentences) // 3), max(2, 2 * len(sentences) // 3))
    last_band = range(max(2, 2 * len(sentences) // 3), len(sentences))

    def pick_best(indices: range) -> None:
        candidates = [index for index in ranked if index in indices]
        if candidates:
            selected.add(candidates[0])

    pick_best(first_band)
    pick_best(middle_band)
    pick_best(last_band)

    for index in ranked:
        if len(selected) >= max_sentences:
            break
        selected.add(index)

    ordered = [sentences[index] for index in sorted(selected)]
    return " ".join(ordered[:max_sentences])
