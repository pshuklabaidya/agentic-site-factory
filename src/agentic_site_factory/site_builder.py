from __future__ import annotations

from html import escape
from pathlib import Path

from agentic_site_factory.models import GeneratedSection, GeneratedSite, SiteSpec, ThemeSpec
from agentic_site_factory.theming import infer_custom_theme


def source_note(section: GeneratedSection) -> str:
    if not section.evidence_sources:
        return ""

    sources = ", ".join(escape(source) for source in section.evidence_sources)
    return f'<p class="source-note">Grounded in: {sources}</p>'


def render_shop_section(section: GeneratedSection) -> str:
    return f"""
    <section id="{escape(section.name)}" class="section">
      <div class="section-label">Commerce Agent</div>
      <h2>{escape(section.heading)}</h2>
      <p>{escape(section.body)}</p>
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

    return f"""
    <section id="{escape(section.name)}" class="section">
      <div class="section-label">{escape(section.name.title())} Agent</div>
      <h2>{escape(section.heading)}</h2>
      <p>{escape(section.body)}</p>
      {source_note(section)}
    </section>
    """


def build_html(
    spec: SiteSpec,
    sections: list[GeneratedSection],
    theme: ThemeSpec | None = None,
) -> GeneratedSite:
    title = f"{spec.author_name} - Official Author Site"
    resolved_theme = theme or infer_custom_theme(spec, documents=[], passages=[])
    rendered_sections = "\n".join(render_section(section) for section in sections)
    nav_links = "".join(
        f'<a href="#{escape(section.name)}">{escape(section.heading)}</a>' for section in sections
    )

    html = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{escape(title)}</title>
  <style>
    :root {{
      --bg: {resolved_theme.background};
      --ink: {resolved_theme.ink};
      --muted: {resolved_theme.muted};
      --card: {resolved_theme.card};
      --accent: {resolved_theme.accent};
      --accent-soft: {resolved_theme.accent_soft};
      --border: {resolved_theme.border};
      --cover-gradient: {resolved_theme.cover_gradient};
    }}
    * {{
      box-sizing: border-box;
    }}
    body {{
      margin: 0;
      font-family: {resolved_theme.font_family};
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
    .shop-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
      gap: 20px;
      margin-top: 24px;
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
  </style>
</head>
<body>
  <header>
    <h1>{escape(spec.author_name)}</h1>
    <p>{escape(spec.website_goal)}</p>
  </header>
  <nav>
    {nav_links}
  </nav>
  <main>
    {rendered_sections}
  </main>
  <footer>
    Generated by Agentic Site Factory. Visual style: {escape(resolved_theme.name)}.
  </footer>
  <script>
    let cartCount = 0;
    function addToCart(itemName) {{
      cartCount += 1;
      document.getElementById('cart-count').textContent = cartCount;
    }}
  </script>
</body>
</html>
"""

    return GeneratedSite(title=title, html=html, sections=sections, theme=resolved_theme)


def save_site(site: GeneratedSite, output_dir: Path) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / "index.html"
    output_path.write_text(site.html, encoding="utf-8")
    return output_path
