from __future__ import annotations

import re
from html import escape
from pathlib import Path

from agentic_site_factory.models import GeneratedSection, GeneratedSite, SiteSpec, ThemeSpec
from agentic_site_factory.text_sanitizer import sanitize_body, sanitize_heading
from agentic_site_factory.theming import infer_custom_theme


def clean_heading(value: str) -> str:
    return sanitize_heading(value, fallback="Section")


def clean_section_id(value: str) -> str:
    cleaned = re.sub(r"[^a-zA-Z0-9_-]+", "-", value.strip().lower())
    cleaned = cleaned.strip("-")
    return cleaned or "section"


def section_filename(section: GeneratedSection) -> str:
    return f"{clean_section_id(section.name)}.html"


def source_note(section: GeneratedSection) -> str:
    if not section.evidence_sources:
        return ""

    sources = ", ".join(escape(sanitize_body(source)) for source in section.evidence_sources)
    return f'<p class="source-note">Grounded in: {sources}</p>'


def render_shop_section(section: GeneratedSection) -> str:
    section_id = clean_section_id(section.name)
    heading = clean_heading(section.heading)
    body = sanitize_body(section.body)

    return f"""
    <section id="{escape(section_id)}" class="section">
      <div class="section-label">Commerce Agent</div>
      <h2>{escape(heading)}</h2>
      <p>{escape(body)}</p>
      {source_note(section)}
      <div class="shop-grid">
        <article class="book-card">
          <div class="book-cover">Book</div>
          <h3>Featured Title</h3>
          <p>Grounded description generated from supplied manuscript material.</p>
          <button onclick="addToCart('Featured Title')">Add to Cart</button>
        </article>
        <article class="book-card">
          <div class="book-cover">Next</div>
          <h3>Upcoming Release</h3>
          <p>Placeholder card for future catalog expansion.</p>
          <button onclick="addToCart('Upcoming Release')">Join Waitlist</button>
        </article>
      </div>
      <div class="cart-box">
        <strong>Demo cart:</strong>
        <span id="cart-count">0</span> selected item(s)
      </div>
    </section>
    """


def render_section(section: GeneratedSection) -> str:
    if section.name == "shop":
        return render_shop_section(section)

    section_id = clean_section_id(section.name)
    heading = clean_heading(section.heading)
    body = sanitize_body(section.body)

    return f"""
    <section id="{escape(section_id)}" class="section">
      <div class="section-label">{escape(sanitize_body(section.name.title()))} Agent</div>
      <h2>{escape(heading)}</h2>
      <p>{escape(body)}</p>
      {source_note(section)}
    </section>
    """


def render_home_intro(spec: SiteSpec, sections: list[GeneratedSection]) -> str:
    section_cards = "\n".join(
        f"""
        <a class="page-card" href="{escape(section_filename(section))}">
          <span>{escape(sanitize_body(section.name.title()))}</span>
          <strong>{escape(clean_heading(section.heading))}</strong>
          <small>{escape(sanitize_body(section.body)[:150])}</small>
        </a>
        """
        for section in sections
    )

    return f"""
    <section class="section home-overview">
      <div class="section-label">Website Builder Output</div>
      <h2>Generated Multi-Page Website</h2>
      <p>{escape(sanitize_body(spec.website_goal))}</p>
      <div class="page-grid">
        {section_cards}
      </div>
    </section>
    """


def render_nav(sections: list[GeneratedSection], current_page: str) -> str:
    home_class = "active" if current_page == "index.html" else ""
    links = [f'<a class="{home_class}" href="index.html">Home</a>']

    for section in sections:
        filename = section_filename(section)
        active_class = "active" if filename == current_page else ""
        links.append(
            f'<a class="{active_class}" href="{escape(filename)}">'
            f"{escape(clean_heading(section.heading))}</a>"
        )

    return "\n".join(links)


def page_css(theme: ThemeSpec) -> str:
    return f"""
    :root {{
      --bg: {theme.background};
      --ink: {theme.ink};
      --muted: {theme.muted};
      --card: {theme.card};
      --accent: {theme.accent};
      --accent-soft: {theme.accent_soft};
      --border: {theme.border};
      --cover-gradient: {theme.cover_gradient};
    }}
    * {{
      box-sizing: border-box;
    }}
    html {{
      scroll-behavior: smooth;
    }}
    body {{
      margin: 0;
      font-family: {theme.font_family};
      color: var(--ink);
      background: var(--bg);
      line-height: 1.6;
    }}
    header {{
      padding: 80px 24px;
      text-align: center;
      background: linear-gradient(135deg, var(--card), var(--accent-soft));
      border-bottom: 1px solid var(--border);
    }}
    header h1 {{
      margin: 0;
      font-size: clamp(2.4rem, 6vw, 5rem);
      line-height: 1;
      letter-spacing: -0.05em;
    }}
    header p {{
      max-width: 760px;
      margin: 24px auto 0;
      color: var(--muted);
      font-size: 1.2rem;
    }}
    nav {{
      display: flex;
      gap: 16px;
      justify-content: center;
      flex-wrap: wrap;
      padding: 16px;
      background: var(--card);
      border-bottom: 1px solid var(--border);
      position: sticky;
      top: 0;
      z-index: 10;
    }}
    nav a {{
      color: var(--ink);
      text-decoration: none;
      font-weight: 700;
      cursor: pointer;
      border-bottom: 2px solid transparent;
      padding-bottom: 2px;
    }}
    nav a.active {{
      color: var(--accent);
      border-bottom-color: var(--accent);
    }}
    main {{
      width: min(1040px, calc(100% - 32px));
      margin: 40px auto;
    }}
    .section {{
      background: var(--card);
      border: 1px solid var(--border);
      border-radius: 24px;
      padding: 32px;
      margin-bottom: 24px;
      box-shadow: 0 14px 30px rgba(15, 23, 42, 0.12);
      scroll-margin-top: 90px;
    }}
    .section-label {{
      color: var(--accent);
      font-size: 0.78rem;
      font-weight: 800;
      letter-spacing: 0.08em;
      text-transform: uppercase;
      margin-bottom: 10px;
    }}
    .section h2 {{
      margin-top: 0;
      font-size: 2rem;
      letter-spacing: -0.03em;
    }}
    .source-note {{
      color: var(--muted);
      font-size: 0.9rem;
      border-top: 1px solid var(--border);
      margin-top: 24px;
      padding-top: 14px;
    }}
    .page-grid,
    .shop-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
      gap: 20px;
      margin-top: 24px;
    }}
    .page-card {{
      display: block;
      border: 1px solid var(--border);
      border-radius: 18px;
      padding: 20px;
      background: var(--bg);
      color: var(--ink);
      text-decoration: none;
      min-height: 170px;
    }}
    .page-card span {{
      color: var(--accent);
      display: block;
      font-size: 0.78rem;
      font-weight: 800;
      letter-spacing: 0.08em;
      text-transform: uppercase;
      margin-bottom: 8px;
    }}
    .page-card strong {{
      display: block;
      font-size: 1.2rem;
      margin-bottom: 12px;
    }}
    .page-card small {{
      color: var(--muted);
      font-size: 0.95rem;
    }}
    .book-card {{
      border: 1px solid var(--border);
      border-radius: 18px;
      padding: 20px;
      background: var(--bg);
    }}
    .book-cover {{
      height: 140px;
      display: grid;
      place-items: center;
      border-radius: 14px;
      background: var(--cover-gradient);
      color: white;
      font-size: 1.7rem;
      font-weight: 800;
      margin-bottom: 16px;
    }}
    button {{
      border: 0;
      border-radius: 999px;
      padding: 10px 18px;
      background: var(--accent);
      color: white;
      font-weight: 700;
      cursor: pointer;
    }}
    .cart-box {{
      margin-top: 20px;
      padding: 16px;
      border-radius: 16px;
      background: var(--accent-soft);
    }}
    footer {{
      text-align: center;
      color: var(--muted);
      padding: 36px 24px;
    }}
    """


def render_page(
    spec: SiteSpec,
    sections: list[GeneratedSection],
    theme: ThemeSpec,
    current_page: str,
    main_content: str,
    page_title: str,
) -> str:
    author_name = sanitize_heading(spec.author_name, fallback="Demo Author")
    website_goal = sanitize_body(spec.website_goal)

    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{escape(page_title)}</title>
  <style>
    {page_css(theme)}
  </style>
</head>
<body>
  <header>
    <h1>{escape(author_name)}</h1>
    <p>{escape(website_goal)}</p>
  </header>
  <nav>
    {render_nav(sections, current_page)}
  </nav>
  <main>
    {main_content}
  </main>
  <footer>
    Generated by Agentic Site Factory. Visual style: {escape(sanitize_body(theme.name))}.
  </footer>
  <script>
    let cartCount = 0;

    function addToCart(itemName) {{
      cartCount += 1;
      const cartCountElement = document.getElementById('cart-count');
      if (cartCountElement) {{
        cartCountElement.textContent = cartCount;
      }}
    }}
  </script>
</body>
</html>
"""


def build_pages(
    spec: SiteSpec,
    sections: list[GeneratedSection],
    theme: ThemeSpec,
) -> dict[str, str]:
    title = f"{sanitize_heading(spec.author_name, fallback='Demo Author')} - Official Author Site"
    all_sections = "\n".join(render_section(section) for section in sections)
    home_content = render_home_intro(spec, sections) + "\n" + all_sections

    pages = {
        "index.html": render_page(
            spec=spec,
            sections=sections,
            theme=theme,
            current_page="index.html",
            main_content=home_content,
            page_title=title,
        )
    }

    for section in sections:
        filename = section_filename(section)
        pages[filename] = render_page(
            spec=spec,
            sections=sections,
            theme=theme,
            current_page=filename,
            main_content=render_section(section),
            page_title=f"{clean_heading(section.heading)} - {title}",
        )

    return pages


def build_html(
    spec: SiteSpec,
    sections: list[GeneratedSection],
    theme: ThemeSpec | None = None,
) -> GeneratedSite:
    title = f"{sanitize_heading(spec.author_name, fallback='Demo Author')} - Official Author Site"
    resolved_theme = theme or infer_custom_theme(spec, documents=[], passages=[])
    pages = build_pages(spec, sections, resolved_theme)
    html = pages["index.html"]

    return GeneratedSite(
        title=title,
        html=html,
        sections=sections,
        theme=resolved_theme,
        pages=pages,
    )


def save_site(site: GeneratedSite, output_dir: Path) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    pages = site.pages or {"index.html": site.html}

    for filename, html in pages.items():
        output_path = output_dir / filename
        output_path.write_text(html, encoding="utf-8")

    return output_dir / "index.html"
