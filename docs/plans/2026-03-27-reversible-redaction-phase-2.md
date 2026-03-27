# reversible-redaction Phase 2 Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Package reversible-redaction as a usable OpenClaw skill with a clean local CLI surface, while keeping redaction deterministic and deferring local small LLM-assisted recognition to the final phase.

**Architecture:** Phase 2 is packaging and integration only. The core redaction engine from Phase 1 remains rule-first and fully local. This phase adds the skill wrapper, packaging metadata, usage docs, and smoke tests so the project can ship as an installable OpenClaw skill without changing the redaction logic itself.

**Tech Stack:** Python 3.11, OpenClaw skill packaging, argparse, pathlib, json, pytest.

---

### Task 1: Define the OpenClaw skill package layout

**Files:**
- Create: `skills/reversible-redaction/SKILL.md`
- Create: `skills/reversible-redaction/package.json` if needed for packaging metadata
- Modify: `README.md`

**Step 1: Write the failing test**

```python
from pathlib import Path

def test_skill_manifest_exists():
    assert Path("skills/reversible-redaction/SKILL.md").exists()
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/test_skill_manifest.py -v`
Expected: FAIL because the skill package does not exist yet.

**Step 3: Write minimal implementation**

- Add a skill manifest that explains the skill’s purpose, inputs, outputs, and constraints
- Document that the skill only consumes redacted text
- Document that local small LLM-assisted recognition is deferred to the final phase

**Step 4: Run test to verify it passes**

Run: `pytest tests/test_skill_manifest.py -v`
Expected: PASS

**Step 5: Commit**

```bash
git add skills/reversible-redaction/SKILL.md README.md
git commit -m "feat: add skill package skeleton"
```

---

### Task 2: Wrap the CLI as the skill-facing entrypoint

**Files:**
- Modify: `src/reversible_redaction/cli.py`
- Create: `tests/test_skill_cli_contract.py`

**Step 1: Write the failing test**

```python
from reversible_redaction.cli import build_parser

def test_skill_cli_contract_supports_redact_and_restore():
    parser = build_parser()
    commands = sorted(parser._subparsers._group_actions[0].choices.keys())
    assert "redact" in commands
    assert "restore" in commands
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/test_skill_cli_contract.py -v`
Expected: FAIL if the CLI contract is not explicit enough.

**Step 3: Write minimal implementation**

- Make parser construction explicit and importable
- Keep CLI behavior stable for skill invocation
- Add helpful usage text for OpenClaw skill docs

**Step 4: Run test to verify it passes**

Run: `pytest tests/test_skill_cli_contract.py -v`
Expected: PASS

**Step 5: Commit**

```bash
git add src/reversible_redaction/cli.py tests/test_skill_cli_contract.py
git commit -m "feat: formalize skill cli contract"
```

---

### Task 3: Document skill usage and operational boundaries

**Files:**
- Modify: `README.md`
- Create: `docs/skill-usage.md`
- Create: `docs/security-boundaries.md`

**Step 1: Write the failing test**

```python
from pathlib import Path

def test_skill_docs_exist():
    assert Path("docs/skill-usage.md").exists()
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/test_skill_docs.py -v`
Expected: FAIL because the docs are not present.

**Step 3: Write minimal implementation**

- Add usage examples for packaging and invocation
- Clearly state that the skill must not receive raw sensitive input
- State that restoration happens locally after LLM output is produced
- State that small LLM-assisted recognition is reserved for the final phase

**Step 4: Run test to verify it passes**

Run: `pytest tests/test_skill_docs.py -v`
Expected: PASS

**Step 5: Commit**

```bash
git add README.md docs/skill-usage.md docs/security-boundaries.md
git commit -m "docs: add skill usage and boundaries"
```

---

### Task 4: Add packaging and installation checks

**Files:**
- Modify: `pyproject.toml`
- Create: `tests/test_packaging.py`

**Step 1: Write the failing test**

```python
from pathlib import Path

def test_pyproject_exposes_console_script():
    assert Path("pyproject.toml").read_text(encoding="utf-8")
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/test_packaging.py -v`
Expected: FAIL if console script metadata is missing or incomplete.

**Step 3: Write minimal implementation**

- Add console script entry point for `reversible-redaction`
- Add package metadata required for a reusable skill package
- Keep dependencies minimal and local-first

**Step 4: Run test to verify it passes**

Run: `pytest tests/test_packaging.py -v`
Expected: PASS

**Step 5: Commit**

```bash
git add pyproject.toml tests/test_packaging.py
git commit -m "feat: add packaging metadata"
```

---

### Task 5: Validate the packaged skill in a clean install flow

**Files:**
- Modify: phase 2 files as needed

**Step 1: Run the full test suite**

Run: `pytest -v`
Expected: All tests pass.

**Step 2: Perform a clean installation smoke test**

Run:

```bash
python -m pip install -e .
reversible-redaction --help
```

Expected:
- package installs cleanly
- CLI help displays redact/restore commands

**Step 3: Verify the skill manifest is readable**

Run:

```bash
cat skills/reversible-redaction/SKILL.md
```

Expected:
- clear purpose
- no raw sensitive data handling in the skill layer

**Step 4: Commit**

```bash
git add .
git commit -m "test: verify skill packaging flow"
```

---

## Execution notes

- Do not introduce local small LLM-assisted recognition in Phase 2.
- Keep Phase 2 focused on packaging, docs, and skill boundaries.
- The final intelligence layer belongs to the last phase only.
- Prefer small commits after each task.
