# Security

## Responsible use
This project is an educational local-only lab for synthetic prompt-injection experiments. Do not enter real credentials, sensitive documents, or third-party data. Do not send exfiltration requests to real services.

## Implemented limits
Streamlit and Ollama are constrained to loopback addresses. The model allowlist is fixed. The app validates UTF-8 text and byte/character limits, blocks pre-validated high-severity attacks in the filtered mode, and has no model tools or mutating functions.

The quarantined mode has two model passes: extraction JSON is schema checked before a fact-only summary pass. This is a mitigation, not a proof of safety.

## Known limitations
Detection is heuristic and can both miss attacks and create false positives. Prompt isolation depends on model behavior and cannot mathematically separate text. Model outputs remain untrusted. Resource caps reduce but do not eliminate availability risk.

## Reporting issues
Do not include secrets or raw untrusted documents in reports. Report only synthetic reproductions and metadata needed to reproduce the issue.
