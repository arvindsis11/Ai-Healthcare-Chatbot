"""LLM provider resolution and startup validation.

This module centralises the logic for:
- Determining the effective base URL for the configured provider
- Validating that a local provider (LM Studio / Ollama) is reachable before
  the application starts accepting requests
"""

import logging
import urllib.error
import urllib.request
from typing import Optional

logger = logging.getLogger(__name__)

# Default base URLs per provider
_PROVIDER_DEFAULTS: dict[str, str] = {
    "openai": "https://api.openai.com/v1",
    "lm-studio": "http://localhost:1234/v1",
    "ollama": "http://localhost:11434/v1",
}

# Providers that require a reachability check on startup
_LOCAL_PROVIDERS = {"lm-studio", "ollama"}


def resolve_base_url(provider: str, override: str = "") -> Optional[str]:
    """Return the base URL to use for the given provider.

    If *override* is non-empty it takes precedence (allows the user to point
    to a custom host, e.g. ``host.docker.internal:1234``).
    For ``openai`` an empty string is returned so that the OpenAI SDK uses its
    built-in default — avoids setting the env var unnecessarily.
    """
    if override:
        return override
    if provider == "openai":
        return None  # let the SDK use its own default
    return _PROVIDER_DEFAULTS.get(provider)


def validate_provider_connectivity(provider: str, base_url: str, timeout: int = 5) -> None:
    """Ping the provider's base URL and log a clear warning if unreachable.

    Only runs for local providers (``lm-studio``, ``ollama``).  For OpenAI
    connectivity failures are surfaced naturally on the first request.

    Args:
        provider:  The value of ``LLM_PROVIDER`` (e.g. ``"lm-studio"``).
        base_url:  The resolved base URL to check.
        timeout:   HTTP request timeout in seconds.
    """
    if provider not in _LOCAL_PROVIDERS:
        return

    # Derive a simple health endpoint: strip trailing /v1 and hit the root
    ping_url = base_url.rstrip("/")
    if ping_url.endswith("/v1"):
        ping_url = ping_url[:-3]

    try:
        req = urllib.request.Request(ping_url, method="GET")
        with urllib.request.urlopen(req, timeout=timeout):
            pass
        logger.info("LLM provider '%s' is reachable at %s", provider, base_url)
    except Exception as exc:  # noqa: BLE001
        logger.warning(
            "LLM provider '%s' does not appear to be running at %s (%s). "
            "Requests will fail until the server is started. "
            "See docs/SETUP.md for setup instructions.",
            provider,
            base_url,
            exc,
        )
