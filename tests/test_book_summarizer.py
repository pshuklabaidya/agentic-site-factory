from agentic_site_factory.book_summarizer import summarize_book_text


def test_summarize_book_text_uses_full_document_signals():
    text = (
        "Elena returns to the coast after her father's death. "
        "She discovers letters hidden in the attic. "
        "Those letters reveal a secret adoption that reshaped the family. "
        "A fire at the old pier forces the town to confront its silence. "
        "By the end, reconciliation comes through shared meals and confession."
    )

    summary = summarize_book_text(text, max_sentences=3)

    assert "letters hidden in the attic" in summary or "secret adoption" in summary
    assert "shared meals and confession" in summary or "fire at the old pier" in summary
