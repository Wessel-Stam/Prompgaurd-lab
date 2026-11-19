# Copilot project instructions: PromptGuard Lab

These instructions apply to all code changes in this repository.

1. Read `IMPLEMENTATIEPLAN_COPILOT.md` and `IMPLEMENTATION_STATUS.md` before making changes. Follow implementation order and every SEC-01–SEC-25 requirement; never silently omit a security requirement.
2. Keep the app **local-only** (Streamlit at 127.0.0.1 and Ollama at http://127.0.0.1:11434). Do not add cloud AI APIs, network exfiltration, model-enabled tools, shell execution or unsafe HTML.
3. Treat user documents, test payloads and model responses as **untrusted**; only app-owned system instructions and security logic are trusted. Separate these in all prompts and tests.
4. Preserve the original `baseline`, `isolated`, `isolated+filter` modes; add `quarantined`. Maintain backwards compatibility with root scripts where possible.
5. Use small typed Python functions, sensible limits, explicit error handling, testable dependency injection for the model client, and clear docstrings.
6. Store only experiment metadata by default. Never add secrets, real personal data, attacker infrastructure or raw documents to logs, CI or repository.
7. No single detector is foolproof. Measure attacks as observable outcomes; distinguish block, timeout, error, model response and manual review.
8. Every new security function requires meaningful pytest tests, including negative tests and false-positive tests. CI must not require a running Ollama server.
9. Before calling a task done, run relevant unit tests/lint/security checks, report exact commands and outputs and update `IMPLEMENTATION_STATUS.md`. Record unverified live experiments as `NOT VERIFIED`.
10. Write original implementations and comments. Do not paste third-party code verbatim, invent test results or misrepresent an isolated prompt as a guarantee.
