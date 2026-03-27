# reversible-redaction

A local reversible document redaction pipeline for enterprise document workflows.

## Goal

- Redact sensitive data before LLM processing
- Keep LLM outputs redacted
- Restore files locally for delivery using a mapping table
- Stay independent from DingTalk or any single chat platform

## Current status

- PRD defined
- Phase 1 implementation in progress

## Workflow

```mermaid
flowchart TD
    A[Input text or file] --> B[Local scanning]
    B --> C[Rule-based redaction]
    C --> D[Mapping table generated]
    D --> E[Redacted text sent to LLM / OpenClaw]
    E --> F[LLM output remains redacted]
    F --> G[Local file restoration]
    G --> H[Final delivery file]
```

## Scope

- Text redaction
- Reversible placeholder mapping
- Local file restoration
- OpenClaw skill integration

See `docs/PRD.md` for the product direction.
