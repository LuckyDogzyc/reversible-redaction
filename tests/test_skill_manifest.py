from pathlib import Path


def test_skill_manifest_exists():
    assert Path("skills/reversible-redaction/SKILL.md").exists()
