.PHONY: install test lint check demo spec-demo app clean

install:
	python -m pip install --upgrade pip
	pip install -e ".[dev]"

test:
	AGENTIC_SITE_FACTORY_DISABLE_OPENAI=1 pytest

lint:
	ruff check .

check: test lint

demo:
	AGENTIC_SITE_FACTORY_DISABLE_OPENAI=1 python scripts/generate_demo_site.py

spec-demo:
	AGENTIC_SITE_FACTORY_DISABLE_OPENAI=1 python scripts/generate_from_spec.py --spec data/sample_specs/elena_vale_author_site.json

app:
	streamlit run app/Home.py

clean:
	rm -rf .pytest_cache .ruff_cache
	find . -type d -name __pycache__ -prune -exec rm -rf {} +
	rm -rf generated_sites/demo_cli generated_sites/latest generated_sites/spec_demo generated_sites/latest_site_bundle.zip
	touch generated_sites/.gitkeep
