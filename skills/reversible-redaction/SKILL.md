---
name: reversible-redaction
description: Local reversible document redaction pipeline for enterprise workflows. Redacts sensitive content before LLM processing, preserves mapping tables, and restores files locally for delivery.
---

# reversible-redaction

## Purpose

Redact sensitive information locally before any LLM sees the content. Keep all LLM-facing inputs and outputs redacted. Restore files locally only at the end of the pipeline when needed.

## Inputs

- Plain text documents
- Markdown documents
- File paths for local redaction / restoration

## Outputs

- Redacted text
- Mapping table
- Restored delivery files

## Constraints

- Must not send raw sensitive content to the LLM
- Must not rely on DingTalk as a hard dependency
- Local small LLM-assisted recognition is reserved for the final phase
- Redaction and restoration must happen locally
