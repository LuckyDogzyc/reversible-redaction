# reversible-redaction PRD

## Background

Enterprise project managers often work with documents containing sensitive data such as IPs, hostnames, serial numbers, people names, and internal project codes. Directly sending this content to an LLM is risky.

This project provides a local reversible redaction pipeline:

1. Ingest text or files locally
2. Detect sensitive content using rules plus a small local LLM
3. Replace sensitive content with placeholders
4. Send only redacted content to OpenClaw / LLM
5. Keep LLM output redacted
6. Restore files locally by applying the mapping table

## Product Goal

- LLM never sees raw sensitive content
- Redaction and restoration happen locally
- Output text stays redacted by default
- File delivery can restore content locally when needed
- The project is platform-agnostic and not tied to DingTalk

## MVP Scope

### Supported formats

- `.txt`
- `.md`
- `.docx`

### Sensitive types

- IP address
- phone number
- ID card number
- email
- hostname
- serial number
- project code
- person name
- organization name

### Key capabilities

- Rule-first scanning
- Local small LLM assisted detection
- Placeholder replacement
- Mapping table generation
- Local file restoration
- Redacted-only LLM output

## Core Modules

- `scanner`
- `redactor`
- `mapping-store`
- `llm-processor`
- `restore-engine`
- `skill-adapter`

## Placeholder Convention

Use: `[[TYPE_001]]`

Examples:
- `[[IP_001]]`
- `[[HOST_002]]`
- `[[PERSON_003]]`

## Phase Roadmap

### Phase 0

- Define sensitive categories
- Define placeholder rules
- Define mapping schema

### Phase 1

- Text redaction
- Text restoration
- CLI support
- Skill interface

### Phase 2

- Full OpenClaw skill packaging
- Ship a usable first version as a packaged skill
- Keep the implementation reusable outside DingTalk

### Phase 3

- `.docx` support
- Preserve paragraph/table formatting

### Phase 4

- `.xlsx` support

### Phase 5

- `.pdf` support

### Phase 6

- Multi-entry integration
- Audit improvements
- Policy tuning and deeper automation

## Success Criteria

- No unauthorized sensitive data reaches the LLM
- Output remains useful for internal collaboration
- Files can be restored locally for delivery
- The pipeline can be reused across platforms
