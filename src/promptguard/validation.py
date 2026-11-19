"""Input and test-data validation."""
from __future__ import annotations

from .config import MAX_BATCH_RUNS, MAX_DOCUMENT_BYTES, MAX_DOCUMENT_CHARS
from .schemas import DocumentInput, TestCase


def validate_document(document: object) -> DocumentInput:
    if not isinstance(document, str):
        raise TypeError("Document must be text.")
    if not document.strip():
        raise ValueError("Document must not be empty.")
    if len(document) > MAX_DOCUMENT_CHARS:
        raise ValueError("Document exceeds the character limit.")
    encoded = document.encode("utf-8")
    if len(encoded) > MAX_DOCUMENT_BYTES:
        raise ValueError("Document exceeds the UTF-8 byte limit.")
    return DocumentInput(document)


def validate_batch_runs(count: int) -> int:
    if isinstance(count, bool) or not isinstance(count, int):
        raise TypeError("Batch run count must be an integer.")
    if count < 1 or count > MAX_BATCH_RUNS:
        raise ValueError("Batch run count is outside the allowed range.")
    return count


def validate_test_case(raw: object) -> TestCase:
    if not isinstance(raw, dict):
        raise TypeError("Test case must be an object.")
    required = ("id", "kind", "category", "name", "language", "document", "attack_goal", "expected_normal_behavior", "evaluation_method")
    if not all(isinstance(raw.get(key), str) for key in required):
        raise ValueError("Test case has missing or invalid fields.")
    if raw["kind"] not in ("attack", "benign"):
        raise ValueError("Test case kind must be attack or benign.")
    validate_document(raw["document"])
    return TestCase(*(raw[key] for key in required))
