from __future__ import annotations

import argparse
import json
from dataclasses import asdict
from pathlib import Path

from .mapping import MappingEntry
from .redactor import redact_text
from .restore import restore_text


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="reversible-redaction")
    subparsers = parser.add_subparsers(dest="command")
    subparsers.required = True

    redact = subparsers.add_parser("redact", help="Redact sensitive content in a text file")
    redact.add_argument("input")
    redact.add_argument("--output", required=True)
    redact.add_argument("--mapping")

    restore = subparsers.add_parser("restore", help="Restore redacted content using a mapping file")
    restore.add_argument("input")
    restore.add_argument("--output", required=True)
    restore.add_argument("--mapping", required=True)

    return parser


def _read_text(path: str) -> str:
    return Path(path).read_text(encoding="utf-8")


def _write_text(path: str, text: str) -> None:
    output = Path(path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(text, encoding="utf-8")


def _write_mapping(path: str, mappings: list[MappingEntry]) -> None:
    output = Path(path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps([asdict(item) for item in mappings], ensure_ascii=False, indent=2), encoding="utf-8")


def _read_mapping(path: str) -> list[MappingEntry]:
    raw = json.loads(Path(path).read_text(encoding="utf-8"))
    return [MappingEntry(**item) for item in raw]


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "redact":
        redacted, mappings = redact_text(_read_text(args.input))
        _write_text(args.output, redacted)
        if args.mapping:
            _write_mapping(args.mapping, mappings)
        return 0

    if args.command == "restore":
        restored = restore_text(_read_text(args.input), _read_mapping(args.mapping))
        _write_text(args.output, restored)
        return 0

    return 1
