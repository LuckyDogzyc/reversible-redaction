from __future__ import annotations

from dataclasses import dataclass
import re
from typing import Iterable


@dataclass(frozen=True)
class Entity:
    kind: str
    original: str
    start: int
    end: int


_PATTERNS: list[tuple[str, re.Pattern[str]]] = [
    ("ip", re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b")),
    ("email", re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b")),
    ("phone", re.compile(r"\b1[3-9]\d{9}\b")),
    ("id_card", re.compile(r"\b\d{17}[0-9Xx]\b")),
    ("serial", re.compile(r"\b[A-Za-z0-9]{6,}(?:-[A-Za-z0-9]{2,})+\b")),
    (
        "hostname",
        re.compile(
            r"\b[a-zA-Z0-9][a-zA-Z0-9_-]*(?:proxy|host|server|srv|node)[a-zA-Z0-9_-]*\b",
            re.IGNORECASE,
        ),
    ),
    (
        "project_code",
        re.compile(r"\b(?:[A-Z]{2,}|[a-z]{2,})[_-][A-Za-z0-9_-]{3,}\b"),
    ),
]


def _dedupe_keep_first(matches: Iterable[Entity]) -> list[Entity]:
    seen: set[tuple[str, str]] = set()
    result: list[Entity] = []
    for entity in matches:
        key = (entity.kind, entity.original)
        if key in seen:
            continue
        seen.add(key)
        result.append(entity)
    return result


def scan_entities(text: str) -> list[Entity]:
    found: list[Entity] = []
    for kind, pattern in _PATTERNS:
        for match in pattern.finditer(text):
            found.append(Entity(kind=kind, original=match.group(0), start=match.start(), end=match.end()))

    found.sort(key=lambda item: (item.start, item.end, item.kind))
    return _dedupe_keep_first(found)
