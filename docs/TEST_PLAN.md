# Test plan

Run unit tests without Ollama:

```bash
python -m pip install -r requirements-dev.txt
python -m pytest -q
python -m ruff check .
python -m bandit -r src app.py detector.py evaluate.py
python -m pip_audit
```

Live tests are opt-in and skipped by default:

```bash
PROMPTGUARD_LIVE_OLLAMA=1 python -m pytest tests/test_live_ollama.py -q
```

Acceptance criteria include 20 synthetic attacks, 10 benign controls, positive and negative detector tests, four pipeline tests, quarantine schema tests, localhost and allowlist checks, safe CSV behavior, and plain-text output handling.
