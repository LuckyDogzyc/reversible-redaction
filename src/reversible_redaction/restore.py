from __future__ import annotations

import re

from .mapping import MappingEntry, mapping_by_token


def restore_text(text: str, mappings: list[MappingEntry]) -> str:
    token_to_original = mapping_by_token(mappings)
    if not token_to_original:
        return text

    tokens = sorted(token_to_original.keys(), key=len, reverse=True)
    pattern = re.compile("|".join(re.escape(item) for item in tokens))

    def replace(match: re.Match[str]) -> str:
        return token_to_original[match.group(0)]

    return pattern.sub(replace, text)
