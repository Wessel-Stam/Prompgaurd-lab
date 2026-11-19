"""Metadata-only storage under a fixed results directory."""
from __future__ import annotations

import csv
from pathlib import Path
from secrets import token_hex

ROOT = Path(__file__).resolve().parents[2]
RESULTS = ROOT / "results"


def safe_csv_text(value: object) -> object:
    if not isinstance(value, str):
        return value
    if value.startswith(("=", "+", "-", "@")):
        return "'" + value
    return value


def write_csv(rows: list[dict[str, object]], destination: Path | None = None) -> Path:
    RESULTS.mkdir(exist_ok=True)
    if destination is not None:
        raise ValueError("Custom result paths are not allowed.")
    name = f"run_utc_{token_hex(8)}.csv"
    destination = RESULTS / name
    if not rows:
        raise ValueError("No result rows to write.")
    with destination.open("x", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows({key: safe_csv_text(value) for key, value in row.items()} for row in rows)
    return destination
