from agentic_site_factory.models import GeneratedSection, GeneratedSite, RetrievedPassage, SiteSpec
from agentic_site_factory.quality import evaluate_site
from agentic_site_factory.theming import infer_custom_theme


def test_evaluate_site_passes_for_persistent_book_cart():
    spec = SiteSpec(author_name="Demo Author", requested_sections=["books", "shop"])
    theme = infer_custom_theme(spec, [], [])
    html = """
    <!doctype html>
    <html>
      <head><title>Demo</title></head>
      <body>
        <main>
          <section>books shop source.txt</section>
          <button onclick="addBookToCart({})">Add to Cart</button>
          <span id="cart-count">0</span>
          <script>
            localStorage.setItem("agenticSiteFactoryCart", "[]");
          </script>
        </main>
      </body>
    </html>
    """
    site = GeneratedSite(
        title="Demo",
        html=html,
        sections=[GeneratedSection(name="books", heading="Books", body="Book list.")],
        theme=theme,
        pages={"index.html": html, "books.html": html},
    )
    passages = [RetrievedPassage(source="source.txt", text="Evidence", score=1.0)]

    report = evaluate_site(spec, site, passages)

    assert report.passed
