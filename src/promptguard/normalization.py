"""Bounded normalization used only for detection."""
from __future__ import annotations

import re
import unicodedata


def normalize_for_detection(text: str, limit: int = 10_000) -> tuple[str, tuple[str, ...]]:
    bounded = text[:limit]
    normalized = unicodedata.normalize("NFKC", bounded).casefold()
    signals: list[str] = []
    if any(unicodedata.category(ch) == "Cf" for ch in bounded):
        signals.append("format_characters")
    if "\u200b" in bounded or "\u200c" in bounded or "\u200d" in bounded:
        signals.append("zero_width_characters")
    if re.search(r"(?:[A-Za-z0-9+/]{12,}={0,2})", bounded):
        signals.append("base64_like")
    if re.search(r"&(?:#\d{1,6}|#x[0-9a-f]+|[a-z][a-z0-9]+);", bounded, re.I):
        signals.append("html_entity_like")
    return normalized, tuple(sorted(set(signals)))
