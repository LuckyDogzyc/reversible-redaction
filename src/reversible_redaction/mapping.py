from __future__ import annotations

from dataclasses import dataclass

from .scanner import Entity


@dataclass(frozen=True)
class MappingEntry:
    token: str
    kind: str
    original: str


def assign_placeholders(entities: list[Entity]) -> list[MappingEntry]:
    counters: dict[str, int] = {}
    mappings: list[MappingEntry] = []
    for entity in entities:
        counters[entity.kind] = counters.get(entity.kind, 0) + 1
        token = f"[[{entity.kind.upper()}_{counters[entity.kind]:03d}]]"
        mappings.append(MappingEntry(token=token, kind=entity.kind, original=entity.original))
    return mappings


def mapping_by_original(mappings: list[MappingEntry]) -> dict[str, str]:
    return {entry.original: entry.token for entry in mappings}


def mapping_by_token(mappings: list[MappingEntry]) -> dict[str, str]:
    return {entry.token: entry.original for entry in mappings}
