from agentic_site_factory.preview_links import create_html_data_url, create_open_site_link


def test_create_html_data_url_returns_html_data_url():
    url = create_html_data_url("<html><body>Hello</body></html>")

    assert url.startswith("data:text/html;base64,")


def test_create_open_site_link_opens_in_new_tab():
    link = create_open_site_link("<html><body>Hello</body></html>")

    assert 'target="_blank"' in link
    assert 'rel="noopener noreferrer"' in link
    assert "Open generated website in new tab" in link
