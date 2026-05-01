from agentic_site_factory.settings import DEFAULT_OPENAI_MODEL, load_openai_settings


def test_load_openai_settings_defaults_to_gpt_5_mini(monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    monkeypatch.delenv("OPENAI_MODEL", raising=False)
    monkeypatch.delenv("AGENTIC_SITE_FACTORY_DISABLE_OPENAI", raising=False)

    settings = load_openai_settings()

    assert not settings.enabled
    assert settings.model == DEFAULT_OPENAI_MODEL


def test_load_openai_settings_reads_environment(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "test-key")
    monkeypatch.setenv("OPENAI_MODEL", "gpt-5-mini")
    monkeypatch.delenv("AGENTIC_SITE_FACTORY_DISABLE_OPENAI", raising=False)

    settings = load_openai_settings()

    assert settings.enabled
    assert settings.api_key == "test-key"
    assert settings.model == "gpt-5-mini"


def test_load_openai_settings_can_disable_openai(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "test-key")
    monkeypatch.setenv("OPENAI_MODEL", "gpt-5-mini")
    monkeypatch.setenv("AGENTIC_SITE_FACTORY_DISABLE_OPENAI", "1")

    settings = load_openai_settings()

    assert not settings.enabled
    assert settings.disabled
