import os

import pytest

pytestmark = pytest.mark.integration


@pytest.mark.skipif(os.environ.get("PROMPTGUARD_LIVE_OLLAMA") != "1", reason="Explicit local Ollama opt-in required")
def test_local_ollama_opt_in():
    import ollama
    result = ollama.chat(model="gemma3:1b", messages=[{"role":"user","content":"Say OK"}], options={"temperature":0})
    assert getattr(result.message, "content", "")
