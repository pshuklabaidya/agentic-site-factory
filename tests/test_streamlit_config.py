from pathlib import Path


def test_static_serving_is_enabled():
    config = Path(".streamlit/config.toml").read_text(encoding="utf-8")

    assert "enableStaticServing = true" in config
