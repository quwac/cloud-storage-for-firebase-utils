import os
from pathlib import Path
import re
from typing import Match, Optional, Tuple, Union, cast
from urllib.parse import unquote

from google.api_core.exceptions import InvalidArgument
from google.cloud.storage import Blob, Client

from csfutils._blob_arg import BlobArg

_BUCKET_NAME = r"([A-Za-z0-9][-A-Za-z0-9._]*[A-Za-z0-9]|[A-Za-z0-9])"

_GS_PATTERN = re.compile(f"^gs://{_BUCKET_NAME}/(.+)$")

_HTTPS_FIREBASESTORAGE_GOOGLEAPIS_COM = re.compile(
    r"^https?://firebasestorage\.googleapis\.com/v[A-Za-z0-9_]+/b/"
    + _BUCKET_NAME
    + r"/o/([^?#]+).*$"
)
_HTTPS_STORAGE_GOOGLEAPIS_COM = re.compile(
    r"^https?://storage\.googleapis\.com/" + _BUCKET_NAME + r"/([^?#]+).*"
)
_HTTPS_STORAGE_CLOUD_GOOGLE_COM = re.compile(
    r"^https?://storage\.cloud\.google\.com/" + _BUCKET_NAME + r"/([^?#]+).*"
)

_HTTPS_PATTERNS = [
    _HTTPS_FIREBASESTORAGE_GOOGLEAPIS_COM,
    _HTTPS_STORAGE_GOOGLEAPIS_COM,
    _HTTPS_STORAGE_CLOUD_GOOGLE_COM,
]

# ---------- public ----------


def init_storage(service_account_key_json_path: Union[str, Path]) -> Client:
    if isinstance(service_account_key_json_path, Path):
        file_path = str(service_account_key_json_path.absolute())
    else:
        file_path = service_account_key_json_path

    if not os.path.exists(file_path):
        raise InvalidArgument(f"{file_path} not found.")

    return cast(
        Client,
        Client.from_service_account_json(file_path),  # type: ignore
    )


def parse_url(url: str) -> Tuple[str, str]:
    """Parse Cloud Storage URL.

    Returns:
        (bucket_name, path)

        example:

        * bucket_name: "example-project.appspot.com"
        * path: "item1/item2/item3/file😊.txt"

    """
    arg = _to_blob_arg(url)

    return arg.bucket_name, arg.path


def ref_from_url(storage: Client, url: str) -> Blob:
    bucket_name, path = parse_url(url)
    bucket = storage.get_bucket(bucket_name)
    blob_or_none = bucket.get_blob(path)
    if blob_or_none is not None:
        return blob_or_none
    else:
        raise ValueError(f"blob may not exists. url={url}")


# ---------- private ----------


def _parse_gs(url: str) -> BlobArg:
    match = _GS_PATTERN.match(url)
    if match is not None:
        bucket_name = match.group(1)
        path = match.group(2)
        return BlobArg(bucket_name=bucket_name, path=path)
    else:
        raise ValueError(f"Not match. url={url}, pattern={_GS_PATTERN.pattern}")


def _parse_https(url: str) -> BlobArg:
    match: Optional[Match[str]] = None
    for pattern in _HTTPS_PATTERNS:
        match = pattern.match(url)
        if match is not None:
            break
    if match is None:
        raise ValueError(f"Not match. url={url}, patterns={_HTTPS_PATTERNS}")

    bucket_name = match.group(1)
    path = unquote(match.group(2))
    return BlobArg(bucket_name=bucket_name, path=path)


def _to_blob_arg(url: str) -> BlobArg:
    if url.startswith("gs://"):
        return _parse_gs(url)
    elif url.startswith("https://") or url.startswith("http://"):
        return _parse_https(url)
    else:
        raise InvalidArgument(f"Invalid url. url={url}")
