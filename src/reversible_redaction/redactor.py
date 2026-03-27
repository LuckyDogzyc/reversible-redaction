from __future__ import annotations

import re

from .mapping import MappingEntry, assign_placeholders, mapping_by_original
from .scanner import scan_entities


def redact_text(text: str) -> tuple[str, list[MappingEntry]]:
    entities = scan_entities(text)
    mappings = assign_placeholders(entities)
    token_by_original = mapping_by_original(mappings)
    if not token_by_original:
        return text, []

    patterns = sorted(token_by_original.keys(), key=len, reverse=True)
    pattern = re.compile("|".join(re.escape(item) for item in patterns))

    def replace(match: re.Match[str]) -> str:
        return token_by_original[match.group(0)]

    return pattern.sub(replace, text), mappings
