from pathlib import Path


def test_examples_are_present():
    assert Path("examples/input.txt").exists()
    assert Path("examples/redacted-example.txt").exists()
    assert Path("examples/mapping.example.json").exists()
