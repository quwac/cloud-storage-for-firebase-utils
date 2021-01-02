import os
from typing import Any, Dict

import yaml


class Arg(object):
    service_account_json_path: str
    bucket_name: str


def _load_arg(file_path: str) -> Arg:
    assert os.path.exists(file_path)

    with open(file_path, "r") as f:
        obj: Dict[str, Any] = yaml.safe_load(f)

    arg = Arg()
    for key, value in obj.items():
        arg.__dict__[key] = value

    return arg


TEST_ARG = _load_arg(".test_args.yaml")
