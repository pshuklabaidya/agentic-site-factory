from agentic_site_factory.ingestion import extract_text_from_txt_bytes


def test_extract_text_from_txt_bytes_cleans_whitespace():
    text = extract_text_from_txt_bytes(b"A   manuscript\nwith   spacing")

    assert text == "A manuscript with spacing"
