from __future__ import annotations

import json
import re
from html import escape
from pathlib import Path

from agentic_site_factory.book_catalog import BookItem, build_book_catalog
from agentic_site_factory.models import (
    GeneratedSection,
    GeneratedSite,
    SiteSpec,
    SourceDocument,
    ThemeSpec,
)
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


def render_cart_box() -> str:
    return """
    <aside class="cart-panel" aria-label="Shopping cart">
      <div>
        <strong>Cart</strong>
        <span id="cart-count">0</span> item(s)
      </div>
      <ul id="cart-items"></ul>
      <button type="button" onclick="clearCart()">Clear Cart</button>
    </aside>
    """


def render_shop_section(section: GeneratedSection, books: list[BookItem]) -> str:
    section_id = clean_section_id(section.name)
    heading = clean_heading(section.heading)
    body = sanitize_body(section.body)

    if books:
        cards = "\n".join(
            f"""
            <article class="book-card">
              <div class="book-cover">{escape(book.title[:18])}</div>
              <h3>{escape(book.title)}</h3>
              <p>{escape(book.summary)}</p>
              <a class="button-link" href="{escape(book.page_filename)}">View Book</a>
              <button type="button" onclick='addBookToCart({json.dumps(book.model_dump())})'>
                Add to Cart
              </button>
            </article>
            """
            for book in books
        )
    else:
        cards = """
        <article class="book-card">
          <div class="book-cover">Book</div>
          <h3>Featured Title</h3>
          <p>Upload book-like documents to generate catalog products.</p>
          <button type="button" onclick="addDemoCartItem()">Add Demo Item</button>
        </article>
        """

    return f"""
    <section id="{escape(section_id)}" class="section">
      <div class="section-label">Commerce Agent</div>
      <h2>{escape(heading)}</h2>
      <p>{escape(body)}</p>
      {source_note(section)}
      <div class="shop-grid">
        {cards}
      </div>
      {render_cart_box()}
    </section>
    """


def render_books_section(section: GeneratedSection, books: list[BookItem]) -> str:
    section_id = clean_section_id(section.name)
    heading = clean_heading(section.heading)
    body = sanitize_body(section.body)

    if books:
        cards = "\n".join(
            f"""
            <a class="page-card" href="{escape(book.page_filename)}">
              <span>Book</span>
              <strong>{escape(book.title)}</strong>
              <small>{escape(book.summary)}</small>
            </a>
            """
            for book in books
        )
    else:
        cards = """
        <div class="empty-state">
          <strong>No book-like uploads detected.</strong>
          <p>Upload manuscripts, novels, memoirs, stories, chapters, essays, or other book-like documents to populate this page.</p>
        </div>
        """

    return f"""
    <section id="{escape(section_id)}" class="section">
      <div class="section-label">Book Catalog</div>
      <h2>{escape(heading)}</h2>
      <p>{escape(body)}</p>
      {source_note(section)}
      <div class="page-grid">
        {cards}
      </div>
    </section>
    """


def render_section(section: GeneratedSection, books: list[BookItem] | None = None) -> str:
    resolved_books = books or []

    if section.name == "shop":
        return render_shop_section(section, resolved_books)

    if section.name == "books":
        return render_books_section(section, resolved_books)

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


def render_book_detail_page_content(book: BookItem) -> str:
    return f"""
    <section class="section book-detail">
      <div class="section-label">Book Page</div>
      <h2>{escape(book.title)}</h2>
      <p>{escape(book.summary)}</p>
      <p class="source-note">Generated from uploaded document: {escape(book.source_name)}</p>
      <div class="book-actions">
        <button type="button" onclick='addBookToCart({json.dumps(book.model_dump())})'>
          Add {escape(book.title)} to Cart
        </button>
        <a class="button-link secondary" href="books.html">Back to Books</a>
      </div>
      {render_cart_box()}
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
    .page-card,
    .book-card {{
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
    .book-cover {{
      height: 140px;
      display: grid;
      place-items: center;
      border-radius: 14px;
      background: var(--cover-gradient);
      color: white;
      font-size: 1.2rem;
      font-weight: 800;
      margin-bottom: 16px;
      text-align: center;
      padding: 12px;
    }}
    button,
    .button-link {{
      border: 0;
      border-radius: 999px;
      padding: 10px 18px;
      background: var(--accent);
      color: white;
      font-weight: 700;
      cursor: pointer;
      display: inline-block;
      margin: 6px 8px 6px 0;
      text-decoration: none;
    }}
    .button-link.secondary {{
      background: var(--muted);
    }}
    .cart-panel {{
      margin-top: 24px;
      padding: 18px;
      border-radius: 18px;
      border: 1px solid var(--border);
      background: var(--accent-soft);
    }}
    .cart-panel ul {{
      margin: 10px 0;
      padding-left: 20px;
    }}
    .empty-state {{
      grid-column: 1 / -1;
      border: 1px dashed var(--border);
      border-radius: 18px;
      padding: 22px;
      background: var(--bg);
    }}
    footer {{
      text-align: center;
      color: var(--muted);
      padding: 36px 24px;
    }}
    """


def cart_script() -> str:
    return """
  <script>
    const CART_KEY = "agenticSiteFactoryCart";

    function readCart() {
      try {
        return JSON.parse(localStorage.getItem(CART_KEY) || "[]");
      } catch (error) {
        return [];
      }
    }

    function writeCart(cart) {
      localStorage.setItem(CART_KEY, JSON.stringify(cart));
      renderCart();
    }

    function addBookToCart(book) {
      const cart = readCart();
      const existing = cart.find((item) => item.id === book.id);

      if (existing) {
        existing.quantity = (existing.quantity || 1) + 1;
      } else {
        cart.push({
          id: book.id,
          title: book.title,
          source_name: book.source_name,
          quantity: 1
        });
      }

      writeCart(cart);
    }

    function addDemoCartItem() {
      addBookToCart({
        id: "demo-book",
        title: "Demo Book",
        source_name: "demo",
        quantity: 1
      });
    }

    function clearCart() {
      writeCart([]);
    }

    function renderCart() {
      const cart = readCart();
      const count = cart.reduce((total, item) => total + (item.quantity || 1), 0);
      document.querySelectorAll("#cart-count").forEach((element) => {
        element.textContent = count;
      });
      document.querySelectorAll("#cart-items").forEach((list) => {
        list.innerHTML = "";

        if (cart.length === 0) {
          const emptyItem = document.createElement("li");
          emptyItem.textContent = "Cart is empty.";
          list.appendChild(emptyItem);
          return;
        }

        cart.forEach((item) => {
          const lineItem = document.createElement("li");
          lineItem.textContent = `${item.title} x ${item.quantity || 1}`;
          list.appendChild(lineItem);
        });
      });
    }

    document.addEventListener("DOMContentLoaded", renderCart);
    renderCart();
  </script>
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
  {cart_script()}
</body>
</html>
"""


def build_pages(
    spec: SiteSpec,
    sections: list[GeneratedSection],
    theme: ThemeSpec,
    documents: list[SourceDocument] | None = None,
) -> dict[str, str]:
    title = f"{sanitize_heading(spec.author_name, fallback='Demo Author')} - Official Author Site"
    books = build_book_catalog(documents or [])
    all_sections = "\n".join(render_section(section, books) for section in sections)
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
            main_content=render_section(section, books),
            page_title=f"{clean_heading(section.heading)} - {title}",
        )

    for book in books:
        pages[book.page_filename] = render_page(
            spec=spec,
            sections=sections,
            theme=theme,
            current_page="books.html",
            main_content=render_book_detail_page_content(book),
            page_title=f"{book.title} - {title}",
        )

    return pages


def build_html(
    spec: SiteSpec,
    sections: list[GeneratedSection],
    theme: ThemeSpec | None = None,
    documents: list[SourceDocument] | None = None,
) -> GeneratedSite:
    title = f"{sanitize_heading(spec.author_name, fallback='Demo Author')} - Official Author Site"
    resolved_theme = theme or infer_custom_theme(spec, documents=[], passages=[])
    pages = build_pages(spec, sections, resolved_theme, documents=documents)
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
