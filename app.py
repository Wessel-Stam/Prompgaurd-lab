"""Streamlit dashboard for the local-only PromptGuard Lab."""
from __future__ import annotations

import streamlit as st

from promptguard.config import ALLOWED_MODELS, MAX_DOCUMENT_CHARS
from promptguard.injection_detector import scan_injection
from promptguard.output_validator import format_compliant, marker_only_success
from promptguard.pipelines import run_document
from promptguard.validation import validate_document

st.set_page_config(page_title="PromptGuard Lab", page_icon="🛡️", layout="wide")
st.warning("Educational local-only lab. Use synthetic data. No defense guarantees safety.")
st.title("🛡️ PromptGuard Lab")

tabs = st.tabs(["Playground", "Compare", "Batch Evaluation", "Results", "Security & About"])

with tabs[0]:
    document = st.text_area("Synthetic document (attacker-controlled)", height=220)
    st.caption(f"{len(document)} / {MAX_DOCUMENT_CHARS} characters")
    model = st.selectbox("Local model", sorted(ALLOWED_MODELS), index=0)
    mode = st.selectbox("Defense mode", ["baseline", "isolated", "isolated+filter", "quarantined"])
    if st.button("Run document", type="primary"):
        try:
            valid = validate_document(document)
            scan = scan_injection(valid.text)
            st.caption(f"Detector: {'suspicious' if scan.is_suspicious else 'not suspicious'}; severity {scan.severity}")
            result = run_document(valid.text, mode, model)
            if result.status == "blocked_by_policy":
                st.warning("Blocked by policy")
            elif result.status in ("timeout", "model_error"):
                st.error("Model error or timeout")
            else:
                st.text(result.response)
                if marker_only_success(result.response):
                    st.error("Exact marker-only objective observed")
                st.caption(f"Format compliant: {format_compliant(result.response)}")
            if result.reason:
                st.caption(result.reason)
        except (TypeError, ValueError) as exc:
            st.error(str(exc))

with tabs[1]:
    st.write("Run the same synthetic document through all four defense modes.")
    comparison = st.text_area("Document for comparison", height=180, key="comparison")
    if st.button("Compare modes"):
        try:
            valid = validate_document(comparison)
            for label, mode_name in zip(st.columns(4), ("baseline", "isolated", "isolated+filter", "quarantined")):
                with label:
                    st.subheader(mode_name)
                    result = run_document(valid.text, mode_name)
                    if result.status == "blocked_by_policy":
                        st.warning("Blocked by policy")
                    elif result.status in ("timeout", "model_error"):
                        st.error("Model error or timeout")
                    else:
                        st.text(result.response)
                    if result.reason:
                        st.caption(result.reason)
        except (TypeError, ValueError) as exc:
            st.error(str(exc))

with tabs[2]:
    st.info("Batch execution starts only when requested. Maximum 120 runs.")
    st.write("Use `python evaluate.py --help` for bounded, reproducible CLI evaluation.")

with tabs[3]:
    st.write("Safe result metadata is written under `results/` by the evaluator.")
    st.caption("Raw documents and responses are excluded unless explicitly opted in.")

with tabs[4]:
    st.write("This tool is experimental and local-only.")
    st.write("No model tools, external fetching, unsafe HTML, or mutating actions are implemented.")
    st.write("OWASP LLM01 Prompt Injection: https://genai.owasp.org/llmrisk/llm01-prompt-injection/")
