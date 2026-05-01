.PHONY: install test lint check demo app clean

install:
	python -m pip install --upgrade pip
	pip install -e ".[dev]"

test:
	pytest

lint:
	ruff check .

check: test lint

demo:
	python scripts/generate_demo_site.py

app:
	streamlit run app/Home.py

clean:
	rm -rf .pytest_cache .ruff_cache
	find . -type d -name __pycache__ -prune -exec rm -rf {} +
	rm -rf generated_sites/demo_cli generated_sites/latest generated_sites/latest_site_bundle.zip
	touch generated_sites/.gitkeep
