"""Strict localhost Ollama client with dependency injection."""
from __future__ import annotations

import time
from typing import Protocol

from .config import ALLOWED_MODELS, MODEL_TIMEOUT_SECONDS, OLLAMA_BASE_URL, MAX_OUTPUT_TOKENS
from .schemas import ModelResult


class ChatClient(Protocol):
    def chat(self, *, model: str, messages: list[dict[str, str]], options: dict[str, object]) -> object: ...


class OllamaError(RuntimeError):
    pass


def verify_localhost(host: str = OLLAMA_BASE_URL) -> None:
    if host != "http://127.0.0.1:11434":
        raise RuntimeError("non_localhost_endpoint")


def create_client(timeout: int = MODEL_TIMEOUT_SECONDS) -> ChatClient:
    """Create the only network client used by the app.

    Passing the host explicitly prevents Ollama's ``OLLAMA_HOST`` environment
    fallback from redirecting requests to a remote service.
    """
    verify_localhost()
    import ollama

    return ollama.Client(host=OLLAMA_BASE_URL, timeout=timeout)


def chat_once(
    messages: list[dict[str, str]],
    model: str,
    client: ChatClient,
    timeout: int = MODEL_TIMEOUT_SECONDS,
) -> ModelResult:
    if model not in ALLOWED_MODELS:
        return ModelResult("model_error", "", "unknown_model", "The selected model is not allowed.", model_invoked=False)
    started = time.monotonic()
    try:
        result = client.chat(
            model=model,
            messages=messages,
            options={"temperature": 0, "num_predict": MAX_OUTPUT_TOKENS, "num_ctx": 4096},
        )
        message = getattr(result, "message", None)
        content = getattr(message, "content", None)
        if not isinstance(content, str):
            return ModelResult("model_error", "", "malformed_model_response", "The model returned an invalid response.", int((time.monotonic() - started) * 1000), True)
        return ModelResult("completed", content, "", "", int((time.monotonic() - started) * 1000), True)
    except TimeoutError:
        return ModelResult("timeout", "", "timeout", "The local model request timed out.", int((time.monotonic() - started) * 1000), True)
    except Exception as exc:
        name = type(exc).__name__
        code = "missing_ollama" if "Connection" in name or "Connect" in name or "Refused" in str(exc) else "ollama_error"
        return ModelResult("model_error", "", code, "The local model could not be reached.", int((time.monotonic() - started) * 1000), True)
