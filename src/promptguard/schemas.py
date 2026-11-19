"""Typed records used by the lab."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal

Mode = Literal["baseline", "isolated", "isolated+filter", "quarantined"]
Status = Literal["completed", "blocked_by_policy", "model_error", "timeout"]


@dataclass(frozen=True)
class DocumentInput:
    text: str


@dataclass(frozen=True)
class ScanResult:
    is_suspicious: bool
    matched_rules: tuple[str, ...]
    severity: str
    reasons: tuple[str, ...]
    normalized_length: int
    signals: tuple[str, ...]


@dataclass(frozen=True)
class ModelResult:
    status: Status
    response: str
    reason_code: str = ""
    reason: str = ""
    latency_ms: int = 0
    model_invoked: bool = False


@dataclass(frozen=True)
class TestCase:
    id: str
    kind: str
    category: str
    name: str
    language: str
    document: str
    attack_goal: str
    expected_normal_behavior: str
    evaluation_method: str


@dataclass(frozen=True)
class EvaluationRow:
    run_id: str
    timestamp_utc: str
    test_id: str
    mode: str
    model: str
    status: str
    reason_code: str
    attempted_objective: str
    marker_only_success: bool
    human_annotation: str = "not_reviewed"
    annotation_source: str = "automatic"
    latency_ms: int = 0
    repetitions: int = 1
    dataset_hash: str = ""
    raw_document: str = field(default="", repr=False)
    raw_response: str = field(default="", repr=False)
