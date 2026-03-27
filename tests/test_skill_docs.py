from pathlib import Path


def test_skill_docs_exist():
    assert Path("docs/skill-usage.md").exists()
    assert Path("docs/security-boundaries.md").exists()
