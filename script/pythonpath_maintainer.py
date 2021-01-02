from pathlib import Path
from typing import Any, Iterable, List, Union

import fire

DEFAULT_IGNORES = ["node_modules", "site-packages"]


def _make_init_py(src_dirs: Iterable[Path]):
    for src_dir in src_dirs:
        if not src_dir.exists():
            return

        _make_init_py_impl(src_dir)


def _ignore_file(name: str) -> bool:
    skip = any(name == default_ignore for default_ignore in DEFAULT_IGNORES)
    if skip:
        return True

    if name.startswith(".") or (name.startswith("__") and name.endswith("__")):
        return True

    return False


def _make_init_py_impl(root: Path):
    name = root.name
    if _ignore_file(name):
        return

    init_py_file = root / "__init__.py"
    if init_py_file.exists():
        for sub_dir in root.iterdir():
            if sub_dir.is_dir():
                _make_init_py_impl(sub_dir)
    else:
        has_py_file = False
        for item in root.iterdir():
            if item.is_file() and item.name.endswith(".py") or item.name.endswith(".pyi"):
                has_py_file = True
                break
        if has_py_file:
            init_py_file.touch()
        for item in root.iterdir():
            if item.is_dir():
                _make_init_py_impl(item)


def _get_module_dirs_impl(roots: Iterable[Path], result: List[Path]):
    for root in roots:
        if root.is_dir():
            init_py_path = root.joinpath("__init__.py")
            if init_py_path.exists():
                result.append(root)
            _get_module_dirs_impl(root.iterdir(), result)


def maintain_pythonpath(
    src_dirs: Union[str, List[str]] = None
):
    assert src_dirs is not None

    temp: List[str] = []
    if type(src_dirs) is str:
        temp = [src_dirs]
    elif isinstance(src_dirs, list):
        temp = src_dirs
    else:
        raise ValueError(f"Illegal src_dirs={src_dirs}")

    src_path_dirs = list(map(lambda src_dir: Path(src_dir).absolute(), temp))

    # make __init__.py
    _make_init_py(src_path_dirs)


if __name__ == "__main__":
    _: Any = fire.Fire(maintain_pythonpath)
