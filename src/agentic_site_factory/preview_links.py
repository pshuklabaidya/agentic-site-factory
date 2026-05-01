from __future__ import annotations

import json


def create_open_site_component(
    html: str,
    label: str = "Open generated website in new tab",
) -> str:
    html_json = json.dumps(html)
    label_json = json.dumps(label)

    return f"""
    <div id="open-site-link-root" style="font-family: sans-serif;"></div>
    <script>
      const html = {html_json};
      const label = {label_json};
      const root = document.getElementById("open-site-link-root");
      const blob = new Blob([html], {{ type: "text/html" }});
      const url = URL.createObjectURL(blob);

      const link = document.createElement("a");
      link.href = url;
      link.target = "_blank";
      link.rel = "noopener noreferrer";
      link.textContent = label;
      link.style.display = "inline-block";
      link.style.padding = "0.75rem 1rem";
      link.style.borderRadius = "999px";
      link.style.background = "#6d28d9";
      link.style.color = "white";
      link.style.fontWeight = "700";
      link.style.textDecoration = "none";

      root.appendChild(link);
    </script>
    """
