from agentic_site_factory.text_sanitizer import sanitize_body, sanitize_heading, sanitize_visible_text


def test_sanitize_visible_text_unwraps_plain_angle_phrases():
    assert sanitize_visible_text("Explore <Books> today") == "Explore Books today"


def test_sanitize_visible_text_removes_html_tags():
    assert sanitize_visible_text("A <strong>bold</strong> claim") == "A bold claim"


def test_sanitize_visible_text_preserves_spaced_angle_content():
    assert sanitize_visible_text("A story < about memory >") == "A story about memory"


def test_sanitize_visible_text_handles_entities():
    assert sanitize_visible_text("Featured &lt;Books&gt;") == "Featured Books"


def test_sanitize_heading_uses_fallback_when_empty():
    assert sanitize_heading("<br>", fallback="Books") == "Books"


def test_sanitize_body_normalizes_whitespace():
    assert sanitize_body("A   line\n\nwith\tspace") == "A line with space"


def test_sanitize_body_removes_leftover_angle_characters():
    assert sanitize_body("A < strange > phrase <") == "A strange phrase"
