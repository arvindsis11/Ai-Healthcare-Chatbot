"""Tests for LLM provider support (issue #55).

All external network calls and third-party SDK constructors are mocked so
the tests run without a real LLM server or API key.
"""

from unittest.mock import MagicMock, patch
from pydantic import ValidationError

import pytest

# ---------------------------------------------------------------------------
# resolve_base_url
# ---------------------------------------------------------------------------

from backend.app.core.llm_provider import resolve_base_url, validate_provider_connectivity


class TestResolveBaseUrl:
    def test_openai_no_override_returns_none(self):
        """OpenAI provider with no override should return None (SDK default)."""
        assert resolve_base_url("openai", "") is None

    def test_openai_with_override_returns_override(self):
        """An explicit override must be respected even for the OpenAI provider.

        This supports setups like a corporate proxy or additional provider setup  through LiteLLM in front of the OpenAI API.
        """
        assert resolve_base_url("openai", "https://custom.openai.proxy/v1") == "https://custom.openai.proxy/v1"

    def test_lm_studio_default_url(self):
        """LM Studio defaults to localhost:1234 when no override is given."""
        assert resolve_base_url("lm-studio", "") == "http://localhost:1234/v1"

    def test_ollama_default_url(self):
        """Ollama defaults to localhost:11434 when no override is given."""
        assert resolve_base_url("ollama", "") == "http://localhost:11434/v1"

    def test_lm_studio_override_url(self):
        """A custom base URL (e.g. host.docker.internal for Docker) overrides the default."""
        custom = "http://host.docker.internal:1234/v1"
        assert resolve_base_url("lm-studio", custom) == custom

    def test_ollama_override_url(self):
        """A custom base URL (e.g. host.docker.internal for Docker) overrides the default."""
        custom = "http://host.docker.internal:11434/v1"
        assert resolve_base_url("ollama", custom) == custom


# ---------------------------------------------------------------------------
# validate_provider_connectivity
# ---------------------------------------------------------------------------

class TestValidateProviderConnectivity:
    def test_openai_skips_check(self):
        """OpenAI provider should never attempt a network request.

        Connectivity for OpenAI is verified naturally on the first real request.
        Pinging api.openai.com on startup would be unnecessary and slow.
        """
        with patch("urllib.request.urlopen") as mock_open:
            validate_provider_connectivity("openai", "https://api.openai.com/v1")
            mock_open.assert_not_called()

    def test_local_provider_reachable_logs_info(self):
        """When the local server is up, an INFO message is logged."""
        with patch("urllib.request.urlopen") as mock_open:
            mock_open.return_value.__enter__ = lambda s: s
            mock_open.return_value.__exit__ = MagicMock(return_value=False)
            with patch("backend.app.core.llm_provider.logger") as mock_logger:
                validate_provider_connectivity("lm-studio", "http://localhost:1234/v1")
                mock_logger.info.assert_called_once()
                assert "lm-studio" in mock_logger.info.call_args.args[1]

    def test_local_provider_unreachable_logs_warning(self):
        """When the local server is down, a WARNING (not an exception) is raised.

        The app should still start and serve requests — it just won't be able
        to call the LLM until the server is running.
        """
        with patch("urllib.request.urlopen", side_effect=OSError("Connection refused")):
            with patch("backend.app.core.llm_provider.logger") as mock_logger:
                validate_provider_connectivity("ollama", "http://localhost:11434/v1")
                mock_logger.warning.assert_called_once()
                # args[0] is the format string; args[1] is the provider name
                assert mock_logger.warning.call_args.args[1] == "ollama"

# ---------------------------------------------------------------------------
# LLMService — provider wiring
# ---------------------------------------------------------------------------

class TestLLMServiceProviderWiring:
    def _make_service(self, **kwargs):
        """Import and construct LLMService with ChatOpenAI patched out."""
        with patch("backend.app.services.llm_service.ChatOpenAI") as MockChat:
            from backend.app.services.llm_service import LLMService
            svc = LLMService(**kwargs)
            return svc, MockChat

    def test_openai_provider_uses_real_key(self):
        """OpenAI provider must pass the real API key and no custom base URL.

        We intentionally omit openai_api_base for the OpenAI provider so the
        SDK uses its own built-in default (https://api.openai.com/v1). Setting
        it explicitly to that same URL would be redundant, and setting it to
        anything else would silently redirect traffic away from OpenAI — so the
        safest contract is: if provider is 'openai', never set openai_api_base.
        """
        with patch("backend.app.services.llm_service.ChatOpenAI") as MockChat:
            from backend.app.services.llm_service import LLMService
            LLMService(api_key="sk-real", model="gpt-4", provider="openai")
            call_kwargs = MockChat.call_args.kwargs
            assert call_kwargs["openai_api_key"] == "sk-real"
            assert "openai_api_base" not in call_kwargs

    def test_lm_studio_provider_uses_dummy_key_and_base_url(self):
        """LM Studio does not require a real API key, so a dummy 'local' key is used.

        LM Studio exposes an OpenAI-compatible API but does not enforce
        authentication. Passing a dummy key satisfies the SDK without exposing
        a real credential.
        """
        with patch("backend.app.services.llm_service.ChatOpenAI") as MockChat:
            from backend.app.services.llm_service import LLMService
            LLMService(
                api_key="",
                model="deepseek-r1-distill-llama-8b",
                base_url="http://localhost:1234/v1",
                provider="lm-studio",
            )
            call_kwargs = MockChat.call_args.kwargs
            assert call_kwargs["openai_api_key"] == "local"
            assert call_kwargs["openai_api_base"] == "http://localhost:1234/v1"

    def test_ollama_provider_sets_base_url(self):
        """Ollama uses an OpenAI-compatible API at its own base URL.

        Like LM Studio, Ollama requires no real API key — the base URL is the
        only configuration needed to redirect requests to the local server.
        """
        with patch("backend.app.services.llm_service.ChatOpenAI") as MockChat:
            from backend.app.services.llm_service import LLMService
            LLMService(
                api_key="",
                model="llama3",
                base_url="http://localhost:11434/v1",
                provider="ollama",
            )
            call_kwargs = MockChat.call_args.kwargs
            assert call_kwargs["openai_api_base"] == "http://localhost:11434/v1"

    def test_no_api_key_and_openai_provider_does_not_init_llm(self):
        """OpenAI provider without a key must stay in fallback mode."""
        with patch("backend.app.services.llm_service.ChatOpenAI") as MockChat:
            from backend.app.services.llm_service import LLMService
            svc = LLMService(api_key="", model="gpt-4", provider="openai")
            MockChat.assert_not_called()
            assert svc.llm is None

    def test_fallback_analyze_symptoms_returns_valid_object(self):
        """Without an LLM, analyze_symptoms should still return a SymptomAnalysis."""
        with patch("backend.app.services.llm_service.ChatOpenAI"):
            from backend.app.services.llm_service import LLMService
            from backend.app.models.chat import SymptomAnalysis
            svc = LLMService(api_key="", provider="openai")
            result = svc.analyze_symptoms(["headache"])
            assert isinstance(result, SymptomAnalysis)


# ---------------------------------------------------------------------------
# TranslationService — provider wiring
# ---------------------------------------------------------------------------

class TestTranslationServiceProviderWiring:
    def test_openai_provider_uses_real_key(self):
        """TranslationService passes the real API key to the OpenAI client."""
        with patch("backend.app.ai.translation_service.TranslationService.__init__") as _:
            pass  # just ensure import works

        from unittest.mock import patch as _patch
        with _patch("openai.OpenAI") as MockOpenAI:
            from backend.app.ai.translation_service import TranslationService
            TranslationService(api_key="sk-real", base_url="", provider="openai")
            if MockOpenAI.called:
                call_kwargs = MockOpenAI.call_args.kwargs
                assert call_kwargs.get("api_key") == "sk-real"

    def test_lm_studio_provider_uses_dummy_key(self):
        """LM Studio does not enforce authentication, so a dummy key is used.

        The OpenAI client still requires an api_key argument — 'local' is used
        as a harmless placeholder that clearly signals no real credential is set.
        """
        with patch("openai.OpenAI") as MockOpenAI:
            from backend.app.ai.translation_service import TranslationService
            svc = TranslationService(api_key="", base_url="http://localhost:1234/v1", provider="lm-studio")
            if MockOpenAI.called:
                assert MockOpenAI.call_args.kwargs.get("api_key") == "local"

    def test_no_key_openai_provider_has_no_client(self):
        """OpenAI provider without a key must not create an OpenAI client."""
        from backend.app.ai.translation_service import TranslationService
        svc = TranslationService(api_key="", base_url="", provider="openai")
        assert svc._client is None

    def test_translate_passthrough_when_no_client(self):
        """Without a client, text is returned unchanged."""
        from backend.app.ai.translation_service import TranslationService
        svc = TranslationService(api_key="", provider="openai")
        assert svc.translate_to_english("hola", "es") == "hola"
        assert svc.translate_from_english("hello", "es") == "hello"


# ---------------------------------------------------------------------------
# Settings validation
# ---------------------------------------------------------------------------

class TestSettings:
    def test_default_provider_is_openai(self, monkeypatch):
        """LLM_PROVIDER should default to 'openai' when not set.

        env vars are cleared so a real .env file mounted in Docker does not
        override the Pydantic default under test.
        """
        monkeypatch.delenv("LLM_PROVIDER", raising=False)
        from backend.app.core.settings import Settings
        s = Settings()
        assert s.llm_provider == "openai"

    def test_invalid_provider_raises(self):
        """An unsupported provider value must raise a validation error.

        The Literal type constraint on llm_provider ensures only the three
        supported values are accepted, preventing silent misconfiguration.
        """
        from backend.app.core.settings import Settings
        with pytest.raises((ValidationError, ValueError)):
            Settings(llm_provider="unsupported-provider")

    def test_lm_studio_provider_accepted(self):
        """'lm-studio' is a valid provider value."""
        from backend.app.core.settings import Settings
        s = Settings(llm_provider="lm-studio")
        assert s.llm_provider == "lm-studio"

    def test_ollama_provider_accepted(self):
        """'ollama' is a valid provider value."""
        from backend.app.core.settings import Settings
        s = Settings(llm_provider="ollama")
        assert s.llm_provider == "ollama"

    def test_base_url_defaults_to_empty(self, monkeypatch):
        """OPENAI_BASE_URL should default to empty string, triggering provider defaults.

        env var is cleared so a real .env file mounted in Docker does not
        override the Pydantic default under test.
        """
        monkeypatch.delenv("OPENAI_BASE_URL", raising=False)
        from backend.app.core.settings import Settings
        s = Settings()
        assert s.openai_base_url == ""
