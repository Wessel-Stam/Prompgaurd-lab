"""Fixed local-only configuration."""
from __future__ import annotations

OLLAMA_BASE_URL = "http://127.0.0.1:11434"
DEFAULT_MODEL = "gemma3:1b"
ALLOWED_MODELS = frozenset({"gemma3:1b", "gemma3:4b", "llama3.2:1b", "llama3.2:3b", "qwen3:1.7b"})
MAX_DOCUMENT_CHARS = 10_000
MAX_DOCUMENT_BYTES = 65_536
MODEL_TIMEOUT_SECONDS = 60
MAX_OUTPUT_TOKENS = 300
MAX_OUTPUT_CHARS = 6_000
MAX_BATCH_RUNS = 120
MAX_REPETITIONS = 5
MAX_CASES = 120

