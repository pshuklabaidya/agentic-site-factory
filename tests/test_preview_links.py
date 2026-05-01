from agentic_site_factory.preview_links import create_open_site_component


def test_create_open_site_component_uses_blob_url_and_new_tab():
    component = create_open_site_component("<html><body>Hello</body></html>")

    assert "Blob" in component
    assert "URL.createObjectURL" in component
    assert 'target = "_blank"' in component
    assert "Open generated website in new tab" in component
