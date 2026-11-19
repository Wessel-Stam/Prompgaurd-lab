# Results guide

The CSV records metadata unless `--include-raw` is explicitly used. Status values distinguish `blocked_by_policy`, `completed`, `timeout`, and `model_error`.

Attack-success metrics exclude model errors and timeouts from attack end-to-end and block-rate denominators. Exact marker-only success is deliberately narrow and is never a claim of complete prompt-injection resistance.

Block rate, false-positive rate, benign completion, median latency, and p95 latency are exploratory. A small hand-built test set cannot estimate real-world or cross-model behavior. Manual review is required for every case.
