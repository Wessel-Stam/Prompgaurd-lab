"""CLI batch runner for PromptGuard Lab."""
from __future__ import annotations

import argparse
import hashlib
import json
from types import SimpleNamespace
from datetime import datetime, timezone
from pathlib import Path
from secrets import token_hex

from promptguard.evaluator import summarize
from promptguard.output_validator import marker_only_success
from promptguard.pipelines import run_document
from promptguard.storage import write_csv
from promptguard.validation import validate_batch_runs, validate_test_case

ROOT = Path(__file__).resolve().parent
CASES = ROOT / "tests" / "attack_cases.json"
MODES = ("baseline", "isolated", "isolated+filter", "quarantined")


def marker_only(answer: str) -> bool:
    return marker_only_success(answer)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", default="gemma3:1b")
    parser.add_argument("--modes", nargs="+", choices=MODES, default=list(MODES))
    parser.add_argument("--repetitions", type=int, default=1)
    parser.add_argument("--max-cases", type=int, default=30)
    parser.add_argument("--include-raw", action="store_true")
    args = parser.parse_args()
    repetitions = max(1, min(args.repetitions, 5))
    validate_batch_runs(len(args.modes) * args.max_cases * repetitions)
    raw = json.loads(CASES.read_text(encoding="utf-8"))
    cases = [validate_test_case(case) for case in raw[:args.max_cases]]
    dataset_bytes = CASES.read_bytes()
    dataset_hash = hashlib.sha256(dataset_bytes).hexdigest()[:16]
    rows: list[dict[str, object]] = []
    for test in cases:
        for mode in args.modes:
            for repeat in range(repetitions):
                print(f"Testing {test.id} in {mode} repetition {repeat + 1}/{repetitions}...")
                try:
                    result = run_document(test.document, mode, args.model)
                    response = result.response
                except Exception:
                    result_status, response = "model_error", ""
                    result = SimpleNamespace(reason_code="model_error", latency_ms=0)
                else:
                    result_status = result.status
                rows.append({
                    "run_id": token_hex(6),
                    "timestamp_utc": datetime.now(timezone.utc).isoformat(),
                    "test_id": test.id,
                    "kind": test.kind,
                    "mode": mode,
                    "model": args.model,
                    "status": result_status,
                    "reason_code": getattr(result, "reason_code", "model_error"),
                    "attempted_objective": test.attack_goal,
                    "marker_only_success": test.kind == "attack" and result_status == "completed" and marker_only(response),
                    "latency_ms": getattr(result, "latency_ms", 0),
                    "dataset_hash": dataset_hash,
                    "annotation_source": "automatic",
                    "human_annotation": "not_reviewed",
                    "raw_document": test.document if args.include_raw else "",
                    "raw_response": response if args.include_raw else "",
                })
    destination = write_csv(rows)
    print(f"Saved metadata to {destination}")
    for mode, metrics in summarize(rows).items():
        print(f"{mode}: " + ", ".join(f"{key}={value if value is not None else 'N/A'}" for key, value in metrics.items()))
    print("Exploratory only; exact marker-only is not a complete attack metric.")


if __name__ == "__main__":
    main()
