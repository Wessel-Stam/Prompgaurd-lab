"""Small, explainable heuristic injection detector."""
from __future__ import annotations

from .normalization import normalize_for_detection
from .schemas import ScanResult

RULES = (
    ("ignore_previous", r"\bignore (?:all )?(?:previous|prior|vorige|eerdere) instructions\b"),
    ("dutch_override", r"\bnegeer (?:de |alle )?(?:vorige|eerdere) instructies\b"),
    ("fake_system", r"(?:\[system(?: override)?\]|<system>|system message|system override)"),
    ("fake_developer", r"(?:\[developer\]|<developer>|developer override|developer message)"),
    ("print_only", r"\b(?:print|return|antwoord|output)\b.{0,30}\b(?:only|uitsluitend|enkel|alleen|exact)\b"),
    ("do_not_summarize", r"\b(?:do not|don't|stop) (?:summar|summarize)\b"),
    ("output_hijack", r"\b(?:exactly|single line|three bullets|rather than bullets)\b"),
    ("delimiter_spoof", r"(?:</?untrusted_|<\|(?:system|developer)\|>|\\x00)"),
)


def scan_injection(document: str) -> ScanResult:
    normalized, signals = normalize_for_detection(document)
    import re

    matched: list[str] = []
    reasons: list[str] = []
    for rule, pattern in RULES:
        if re.search(pattern, normalized, re.I):
            matched.append(rule)
            reasons.append(f"Heuristic rule matched: {rule}")
    for signal in signals:
        reasons.append(f"Obfuscation signal: {signal}")
    severity = "high" if any(r in matched for r in ("ignore_previous", "dutch_override", "fake_system", "fake_developer")) else (
        "medium" if matched or signals else "low"
    )
    return ScanResult(bool(matched or signals), tuple(matched), severity, tuple(reasons), len(normalized), signals)


def detect_pattern(document: str) -> str | None:
    result = scan_injection(document)
    return result.matched_rules[0] if result.matched_rules else None
