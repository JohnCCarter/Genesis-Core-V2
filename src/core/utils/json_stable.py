from __future__ import annotations

import json
from typing import TypeAlias

JsonScalar: TypeAlias = str | int | float | bool | None
JsonValue: TypeAlias = JsonScalar | list["JsonValue"] | dict[str, "JsonValue"]
JsonObject: TypeAlias = dict[str, JsonValue]


def json_dumps_stable(payload: JsonObject) -> str:
    """Serialize a JSON object deterministically (sorted keys, trailing newline).

    Shared so packet/trace surfaces can reuse the same stable serialization as the
    intelligence event layer without depending on the intelligence domain.
    """

    return json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False) + "\n"


__all__ = ["JsonObject", "JsonScalar", "JsonValue", "json_dumps_stable"]
