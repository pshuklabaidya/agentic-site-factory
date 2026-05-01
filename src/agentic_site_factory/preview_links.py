from __future__ import annotations

import base64
from html import escape


def create_html_data_url(html: str) -> str:
    encoded = base64.b64encode(html.encode("utf-8")).decode("ascii")
    return f"data:text/html;base64,{encoded}"


def create_open_site_link(
    html: str,
    label: str = "Open generated website in new tab",
) -> str:
    url = create_html_data_url(html)
    return (
        f'<a href="{escape(url)}" target="_blank" rel="noopener noreferrer">'
        f"{escape(label)}</a>"
    )
