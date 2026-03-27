# reversible-redaction Phase 1 Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Build a local reversible redaction CLI for plain text files that redacts sensitive entities, preserves a mapping table, and can restore files locally.

**Architecture:** A small Python package with three layers: scanner, redactor, and restore engine. The CLI orchestrates file loading, redaction, mapping export, and optional restoration. The implementation stays dependency-light (stdlib + pytest) so it can later be embedded into an OpenClaw skill or any other entrypoint.

**Tech Stack:** Python 3.11, argparse, re, dataclasses, json, pathlib, pytest.

---

### Task 1: Bootstrap the Python package and test harness

**Files:**
- Create: `pyproject.toml`
- Create: `src/reversible_redaction/__init__.py`
- Create: `src/reversible_redaction/cli.py`
- Create: `tests/test_imports.py`

**Step 1: Write the failing test**

```python
from reversible_redaction import __version__

def test_package_imports():
    assert __version__
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/test_imports.py -v`
Expected: FAIL with `ModuleNotFoundError` or missing package import.

**Step 3: Write minimal implementation**

- Add package metadata in `pyproject.toml`
- Add `__version__` in `src/reversible_redaction/__init__.py`
- Add a minimal CLI stub in `src/reversible_redaction/cli.py`

**Step 4: Run test to verify it passes**

Run: `pytest tests/test_imports.py -v`
Expected: PASS

**Step 5: Commit**

```bash
git add pyproject.toml src/reversible_redaction/__init__.py src/reversible_redaction/cli.py tests/test_imports.py
git commit -m "chore: bootstrap reversible-redaction package"
```

---

### Task 2: Implement entity scanning and mapping generation

**Files:**
- Create: `src/reversible_redaction/scanner.py`
- Create: `src/reversible_redaction/mapping.py`
- Create: `tests/test_scanner.py`

**Step 1: Write the failing test**

```python
from reversible_redaction.scanner import scan_entities

def test_scan_entities_detects_ips_and_hosts():
    text = "Server 10.1.2.3 runs kpw_proxy_72 and backup 10.1.2.3"
    entities = scan_entities(text)
    kinds = [e.kind for e in entities]
    assert "ip" in kinds
    assert "hostname" in kinds
    assert len([e for e in entities if e.original == "10.1.2.3"]) == 1
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/test_scanner.py -v`
Expected: FAIL because scanner module and entity model do not exist yet.

**Step 3: Write minimal implementation**

- Implement a small `Entity` dataclass
- Add regex-based detection for the first phase:
  - IP address
  - phone number
  - ID number
  - email
  - hostname / proxy names
  - serial-like identifiers
- Add deterministic token assignment helper in `mapping.py`

**Step 4: Run test to verify it passes**

Run: `pytest tests/test_scanner.py -v`
Expected: PASS

**Step 5: Commit**

```bash
git add src/reversible_redaction/scanner.py src/reversible_redaction/mapping.py tests/test_scanner.py
git commit -m "feat: add entity scanning and mapping"
```

---

### Task 3: Implement redaction and restoration for plain text

**Files:**
- Create: `src/reversible_redaction/redactor.py`
- Create: `src/reversible_redaction/restore.py`
- Create: `tests/test_redactor.py`
- Create: `tests/test_restore.py`

**Step 1: Write the failing test**

```python
from reversible_redaction.redactor import redact_text
from reversible_redaction.restore import restore_text

def test_redact_and_restore_round_trip():
    original = "IP 10.1.2.3 belongs to kpw_proxy_72"
    redacted, mapping = redact_text(original)
    assert "10.1.2.3" not in redacted
    assert "kpw_proxy_72" not in redacted
    restored = restore_text(redacted, mapping)
    assert restored == original
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/test_redactor.py tests/test_restore.py -v`
Expected: FAIL because redact/restore functions do not exist yet.

**Step 3: Write minimal implementation**

- Replace sensitive values with stable placeholders like `[[IP_001]]`
- Return a mapping table from placeholder to original text
- Implement restore by applying the mapping table in reverse
- Keep text-only behavior for phase 1

**Step 4: Run test to verify it passes**

Run: `pytest tests/test_redactor.py tests/test_restore.py -v`
Expected: PASS

**Step 5: Commit**

```bash
git add src/reversible_redaction/redactor.py src/reversible_redaction/restore.py tests/test_redactor.py tests/test_restore.py
git commit -m "feat: add reversible text redaction"
```

---

### Task 4: Add the CLI for file redaction and restoration

**Files:**
- Modify: `src/reversible_redaction/cli.py`
- Modify: `pyproject.toml`
- Create: `tests/test_cli.py`

**Step 1: Write the failing test**

```python
from pathlib import Path
from reversible_redaction.cli import main

def test_cli_redacts_and_writes_output(tmp_path, monkeypatch):
    input_file = tmp_path / "input.txt"
    output_file = tmp_path / "output.txt"
    input_file.write_text("10.1.2.3 uses kpw_proxy_72", encoding="utf-8")
    monkeypatch.setattr("sys.argv", ["reversible-redaction", "redact", str(input_file), "--output", str(output_file)])
    assert main() == 0
    assert output_file.exists()
    assert "10.1.2.3" not in output_file.read_text(encoding="utf-8")
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/test_cli.py -v`
Expected: FAIL because CLI subcommands are not implemented yet.

**Step 3: Write minimal implementation**

- Add `redact` and `restore` subcommands
- Support file input/output paths
- Support optional mapping output file
- Return exit code 0 on success, non-zero on validation failure
- Expose a console script entry point in `pyproject.toml`

**Step 4: Run test to verify it passes**

Run: `pytest tests/test_cli.py -v`
Expected: PASS

**Step 5: Commit**

```bash
git add src/reversible_redaction/cli.py pyproject.toml tests/test_cli.py
git commit -m "feat: add reversible-redaction CLI"
```

---

### Task 5: Add examples and usage docs for phase 1

**Files:**
- Modify: `README.md`
- Create: `examples/input.txt`
- Create: `examples/redacted-example.txt`
- Create: `examples/mapping.example.json`

**Step 1: Write the failing test**

```python
from pathlib import Path

def test_examples_are_present():
    assert Path("examples/input.txt").exists()
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/test_examples.py -v`
Expected: FAIL because examples and docs are not added yet.

**Step 3: Write minimal implementation**

- Add a short README with install/run examples
- Add one sample input file, one redacted output file, and one mapping example
- Keep the examples plain text and easy to understand

**Step 4: Run test to verify it passes**

Run: `pytest tests/test_examples.py -v`
Expected: PASS

**Step 5: Commit**

```bash
git add README.md examples/input.txt examples/redacted-example.txt examples/mapping.example.json
git commit -m "docs: add reversible-redaction examples"
```

---

### Task 6: Verification pass and release prep

**Files:**
- Modify: all phase 1 files as needed

**Step 1: Run the full test suite**

Run: `pytest -v`
Expected: All tests pass.

**Step 2: Run a manual smoke test**

Run:

```bash
reversible-redaction redact examples/input.txt --output /tmp/redacted.txt --mapping /tmp/mapping.json
reversible-redaction restore /tmp/redacted.txt --mapping /tmp/mapping.json --output /tmp/restored.txt
```

Expected:
- `/tmp/redacted.txt` contains placeholders only
- `/tmp/restored.txt` matches the original input

**Step 3: Commit**

```bash
git add .
git commit -m "test: verify phase 1 reversible redaction flow"
```

---

## Execution notes

- Keep all LLM-facing inputs redacted only.
- Do not add docx/xlsx/pdf support in phase 1.
- Prefer small commits after each task.
- If a test needs fixture data, keep it tiny and obvious.
