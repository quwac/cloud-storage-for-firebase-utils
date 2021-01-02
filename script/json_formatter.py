import json
from typing import Any, Dict, List, cast

import fire
import json5


def _parse_json_pointer(json_pointer: str) -> List[str]:
    text = json_pointer
    if text.startswith("/"):
        text = text[1:]
    if text.endswith("/"):
        end_index = len(text) - 1
        text = text[0:end_index]

    return text.split(",")


def _sort_set(obj: Any, json_pointer: str):
    segments = _parse_json_pointer(json_pointer)

    target_obj = obj
    for segment in segments:
        target_obj = cast(Dict[str, Any], target_obj)[segment]

    target_array = cast(List[str], target_obj)

    target_array.sort()


def format_json(json_file_path: str, as_set_paths: List[str] = []):
    with open(json_file_path, "r") as f:
        obj: Any = json5.load(f, allow_duplicate_keys=False)

    for set_path in as_set_paths:
        _sort_set(obj, set_path)

    formatted = json.dumps(obj, sort_keys=True, ensure_ascii=False, indent=4)
    print(formatted)  # noqa: T001


if __name__ == "__main__":
    _: Any = fire.Fire(format_json)
