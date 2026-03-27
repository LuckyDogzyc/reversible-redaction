from __future__ import annotations

import argparse


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


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    parser.parse_args(argv)
    return 0
