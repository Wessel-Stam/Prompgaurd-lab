# Implementation status

This repository contains the implemented local-only educational lab. No live Ollama experiments or final human security review are claimed as complete.

The authoritative specification is `IMPLEMENTATIEPLAN_COPILOT.md`.

## Implementation phases
- [x] Phase 1: Inventory, setup and scaffold
- [x] Phase 2: Threat model and experiment contract
- [x] Phase 3: Input validation and detection
- [x] Phase 4: Local Ollama client and bounded execution
- [x] Phase 5: Four defensive modes
- [x] Phase 6: Output validation and classification
- [x] Phase 7: 20 attacks + 10 benign cases
- [x] Phase 8: Evaluation and metrics
- [x] Phase 9: Streamlit dashboard
- [x] Phase 10: Automated tests and CI
- [x] Phase 11: Reports and documentation
- [ ] Phase 12: Final security review and acceptance

## Required security controls
- [x] SEC-01 — implemented and covered by unit tests or explicit documented limitation
- [x] SEC-02 — implemented and covered by unit tests or explicit documented limitation
- [x] SEC-03 — implemented and covered by unit tests or explicit documented limitation
- [x] SEC-04 — implemented and covered by unit tests or explicit documented limitation
- [x] SEC-05 — implemented and covered by unit tests or explicit documented limitation
- [x] SEC-06 — implemented and covered by unit tests or explicit documented limitation
- [x] SEC-07 — implemented and covered by unit tests or explicit documented limitation
- [x] SEC-08 — implemented and covered by unit tests or explicit documented limitation
- [x] SEC-09 — implemented and covered by unit tests or explicit documented limitation
- [x] SEC-10 — implemented and covered by unit tests or explicit documented limitation
- [x] SEC-11 — implemented and covered by unit tests or explicit documented limitation
- [x] SEC-12 — implemented and covered by unit tests or explicit documented limitation
- [x] SEC-13 — implemented and covered by unit tests or explicit documented limitation
- [x] SEC-14 — implemented and covered by unit tests or explicit documented limitation
- [x] SEC-15 — implemented and covered by unit tests or explicit documented limitation
- [x] SEC-16 — implemented and covered by unit tests or explicit documented limitation
- [x] SEC-17 — implemented and covered by unit tests or explicit documented limitation
- [x] SEC-18 — implemented and covered by unit tests or explicit documented limitation
- [x] SEC-19 — implemented and covered by unit tests or explicit documented limitation
- [x] SEC-20 — implemented and covered by unit tests or explicit documented limitation
- [x] SEC-21 — implemented and covered by unit tests or explicit documented limitation
- [x] SEC-22 — implemented and covered by unit tests or explicit documented limitation
- [x] SEC-23 — implemented and covered by unit tests or explicit documented limitation
- [x] SEC-24 — implemented and covered by unit tests or explicit documented limitation
- [x] SEC-25 — implemented and covered by unit tests or explicit documented limitation

## Verification
- [x] Unit tests executed successfully: `python -m pytest -q` — 47 passed, 1 integration test skipped (Python 3.12; Python 3.11 is CI-only in this environment).
- [x] Lint and static security checks pass: `python -m ruff check .` passed; `python -m bandit -r src app.py detector.py evaluate.py` passed.
- [x] Dependency audit: after upgrading pip, `python -m pip_audit` reported no known vulnerabilities; the local audit also notes the project is not published to PyPI.
- [ ] Local Ollama integration run completed (NOT VERIFIED).
- [ ] False-positive and attack-success experiments measured (NOT VERIFIED: requires local model).
- [ ] Human review completed (NOT VERIFIED).

## Review follow-up

- Ollama 0.6.1 requests now use `ollama.Client(host="http://127.0.0.1:11434", timeout=60)` and call the SDK-compatible `chat()` signature without a per-call timeout.
- `OLLAMA_HOST` is tested as unable to redirect the explicit client host.
- CI upgrades pip before audit and pins patched Streamlit, Pillow, PyArrow, and setuptools versions.
- The previous CI run `44459664695` failed dependency auditing; its pull-request run `44459669759` was `action_required` before these fixes. A new run is required after this push.

**Rule:** Only check off an item once it exists, passes applicable tests and the exact results are recorded. Do not invent measurements.
