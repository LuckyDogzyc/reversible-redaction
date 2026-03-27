import json
from pathlib import Path

from reversible_redaction.cli import main


def test_cli_redacts_and_writes_output(tmp_path, monkeypatch):
    input_file = tmp_path / "input.txt"
    output_file = tmp_path / "output.txt"
    mapping_file = tmp_path / "mapping.json"
    input_file.write_text("10.1.2.3 uses kpw_proxy_72", encoding="utf-8")
    monkeypatch.setattr(
        "sys.argv",
        ["reversible-redaction", "redact", str(input_file), "--output", str(output_file), "--mapping", str(mapping_file)],
    )

    assert main() == 0
    assert output_file.exists()
    assert mapping_file.exists()
    redacted = output_file.read_text(encoding="utf-8")
    assert "10.1.2.3" not in redacted
    assert "kpw_proxy_72" not in redacted
    mappings = json.loads(mapping_file.read_text(encoding="utf-8"))
    assert mappings


def test_cli_restores_from_mapping(tmp_path, monkeypatch):
    input_file = tmp_path / "input.txt"
    redacted_file = tmp_path / "redacted.txt"
    mapping_file = tmp_path / "mapping.json"
    restored_file = tmp_path / "restored.txt"
    input_file.write_text("10.1.2.3 uses kpw_proxy_72", encoding="utf-8")

    monkeypatch.setattr(
        "sys.argv",
        ["reversible-redaction", "redact", str(input_file), "--output", str(redacted_file), "--mapping", str(mapping_file)],
    )
    assert main() == 0

    monkeypatch.setattr(
        "sys.argv",
        ["reversible-redaction", "restore", str(redacted_file), "--output", str(restored_file), "--mapping", str(mapping_file)],
    )
    assert main() == 0
    assert restored_file.read_text(encoding="utf-8") == input_file.read_text(encoding="utf-8")
