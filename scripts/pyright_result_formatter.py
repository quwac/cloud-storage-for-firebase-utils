import json
import os
from typing import Any, Dict, List, Optional

import fire
from simple_chalk import chalk


def format_pyright_result(
    obj: Dict[str, Any]
) -> List[Any]:
    result: List[Any] = []

    diagnostics: List[Dict[str, Any]] = obj['diagnostics']
    for i, diagnostic in enumerate(diagnostics):
        file_name: str = diagnostic['file']
        severity: str = diagnostic['severity']
        message: str = diagnostic['message']
        start: Dict[str, Any] = diagnostic['range']['start']
        line: int = start['line']
        character: int = start['character']
        rule: str = diagnostic['rule']

        message = f'[{i + 1}] {file_name}:{line + 1}:{character + 1}: {rule} {message}'

        if severity == 'error':
            board = chalk.red(message)
        elif severity == "warning":
            board = chalk.yellow(message)
        else:
            board = message

        result.append(board)

    return result


def _main(
    pyright_result_json: Optional[str] = None
):
    assert pyright_result_json is not None

    if os.path.exists(pyright_result_json):
        with open(pyright_result_json, 'r') as f:
            obj: Dict[str, Any] = json.load(f)
    else:
        obj: Dict[str, Any] = json.loads(pyright_result_json)

    messages = format_pyright_result(obj)

    for mes in messages:
        print(mes)


if __name__ == "__main__":
    _: Any = fire.Fire(_main)
