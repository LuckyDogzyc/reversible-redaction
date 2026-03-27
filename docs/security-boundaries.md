# Security Boundaries

## Hard boundaries

- Raw sensitive content must stay local
- LLM-facing prompts and responses must remain redacted
- Mapping tables are local artifacts only
- Restoration happens only after model processing

## Phase 2 boundary

Phase 2 is packaging and integration only. It must not add local small LLM-assisted recognition or final-pass entity refinement.

## Future boundary

The final-phase recognition layer will be added later, after the skill package is stable.
