from pathlib import Path


def test_pyproject_exposes_console_script():
    text = Path("pyproject.toml").read_text(encoding="utf-8")
    assert "[project.scripts]" in text
    assert 'reversible-redaction = "reversible_redaction.cli:main"' in text
