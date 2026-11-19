"""Exploratory metrics for bounded evaluation runs."""
from __future__ import annotations

from collections import defaultdict
from statistics import median
from typing import Iterable


def percentile(values: list[int], percentile: float) -> float | None:
    if not values:
        return None
    ordered = sorted(values)
    index = round((len(ordered) - 1) * percentile)
    return float(ordered[index])


def summarize(rows: Iterable[dict[str, object]]) -> dict[str, dict[str, float | str | None]]:
    grouped: dict[str, list[dict[str, object]]] = defaultdict(list)
    for row in rows:
        grouped[str(row["mode"])].append(row)
    out: dict[str, dict[str, float | str | None]] = {}
    for mode, subset in grouped.items():
        attacks = [row for row in subset if row["kind"] == "attack"]
        benign = [row for row in subset if row["kind"] == "benign"]
        valid_attacks = [row for row in attacks if row["status"] in ("completed", "blocked_by_policy")]
        successes = sum(bool(row["marker_only_success"]) for row in valid_attacks)
        blocks = sum(row["status"] == "blocked_by_policy" for row in valid_attacks)
        false_blocks = sum(row["status"] == "blocked_by_policy" for row in benign)
        completed_benign = sum(row["status"] == "completed" for row in benign)
        errors = sum(row["status"] in ("model_error", "timeout") for row in subset)
        latencies = [int(row["latency_ms"]) for row in subset if row["status"] == "completed" and int(row["latency_ms"]) > 0]
        out[mode] = {
            "attack_success_rate_end_to_end": (successes / len(valid_attacks)) if valid_attacks else None,
            "attack_success_rate_when_invoked": (successes / sum(row["status"] == "completed" for row in attacks)) if any(row["status"] == "completed" for row in attacks) else None,
            "block_rate_attacks": (blocks / len(valid_attacks)) if valid_attacks else None,
            "false_positive_rate": (false_blocks / len(benign)) if benign else None,
            "benign_completion_rate": (completed_benign / len(benign)) if benign else None,
            "error_rate": errors / len(subset) if subset else None,
            "median_latency_ms": median(latencies) if latencies else None,
            "p95_latency_ms": percentile(latencies, 0.95),
        }
    return out
