"""Backward-compatible exports for the original starter API."""
from __future__ import annotations

from promptguard.pipelines import run_document

MODEL = "gemma3:1b"


def summarize_document(document: str, mode: str, model: str = MODEL) -> dict[str, str]:
    result = run_document(document, mode, model)
    status = "blocked" if result.status == "blocked_by_policy" else ("error" if result.status in ("timeout", "model_error") else "ok")
    return {"status": status, "response": result.response, "reason": result.reason}
