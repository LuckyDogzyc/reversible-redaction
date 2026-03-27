# Skill Usage

`reversible-redaction` is packaged as an OpenClaw skill for local reversible document processing.

## What it does

- Accepts redacted text or file paths from the local pipeline
- Produces redacted outputs only
- Leaves file restoration to the local restore engine

## What it does not do

- It does not accept raw sensitive content as the preferred input
- It does not perform final recovery of sensitive values inside the model
- It does not include final-phase local small LLM-assisted recognition

## Intended integration

The skill is meant to be called by OpenClaw orchestration after redaction has already happened locally.
