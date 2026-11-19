# Implement PromptGuard Lab from the complete security specification

## Goal
Implement the entire locally run PromptGuard Lab project, starting from the existing starter code. The repository contains the authoritative specification `IMPLEMENTATIEPLAN_COPILOT.md` and permanent engineering requirements in `.github/copilot-instructions.md`.

## Scope and implementation sequence
1. Audit the existing repository and create `IMPLEMENTATION_STATUS.md` with every phase and checkbox from the plan.
2. Implement all security requirements SEC-01 through SEC-25, including localhost-only Ollama and UI, model allowlisting, input validation, prompt/data isolation, heuristic detection, quarantined pipeline, no tools, output validation, strict resource bounds, safe logging, safe CSV export, and defensive error handling.
3. Implement all four defense modes: baseline, isolated, isolated+filter, quarantined.
4. Build the Streamlit user interface, deterministic test-case runner, evaluation metrics, output review workflow, and reporting.
5. Supply at least 20 distinct attack examples, 10 benign controls, and 30 meaningful automated tests. Add linting, dependency audit, SAST, and CI checks.
6. Provide original implementation, reproducible setup, `docs/SECURITY.md`, a threat model, test plan, results guide, limitations, and clear licensing/attribution of third-party dependencies.

## Required security behavior
Never expose Ollama or Streamlit to external interfaces; do not add cloud APIs, shell/browser/filesystem tools for the model, URL fetching, actual exfiltration, real credentials or sensitive testing data. Treat all documents and model outputs as untrusted. Do not promise prompt injection can be perfectly eliminated. Never commit secrets or raw model input/output to the repository.

## Verification and reporting
- Preserve compatibility with `app.py`, `detector.py`, `evaluate.py` unless a documented migration is necessary.
- Use independent unit tests; CI cannot rely on local Ollama being available.
- Log exact commands and results, and distinguish errors/timeouts from blocked attacks.
- Mark Ollama-dependent tests **NOT VERIFIED** until actually run with a local model.
- Do not claim completion for missing implementations, placeholders, skipped tests, or synthetic data.
- Submit a pull request for human review. Do **not** merge it automatically.

**The implementation plan is longer and more detailed than this issue: follow it in full.**