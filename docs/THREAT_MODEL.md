# Threat model

## Assets
The lab protects synthetic documents, local experiment metadata, model availability, and the local machine from accidental network or mutating actions.

## Actors
The attacker controls only document text. The user controls the local UI and model choices; the app owner controls trusted prompts and policies.

## Entry points
The text area, test dataset, and exported test results are untrusted inputs or outputs. No document is fetched from a URL.

## Trust boundaries
App-owned prompts and validators are trusted. Documents and model responses are untrusted. The isolated and quarantined modes are behavioral mitigations, not security guarantees.

## Attacker capabilities
The attacker may use instruction overrides, fake roles, Unicode or delimiter tricks, and dummy exfiltration requests. They cannot select arbitrary hosts or model tools in this implementation.

## Non-goals
This lab does not prevent every prompt injection, execute network operations, use real credentials, or protect a remote service. Ollama and Streamlit must remain local.

## Controls
The implementation uses local endpoints, model allowlisting, input limits, normalization, heuristic detection, random serialization boundaries, output limits, a quarantined extraction pass, metadata-only logging, and fixed-path CSV export.
