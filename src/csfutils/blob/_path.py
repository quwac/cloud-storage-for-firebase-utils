from typing import List, Optional, Union
from urllib.parse import quote

from google.cloud.storage import Blob

from csfutils._client import parse_url
from csfutils.blob._access_token import get_access_token
from csfutils.url_type import UrlType

# ---------- public ----------


def get_download_url(
    blob: Blob, url_type: UrlType = UrlType.FIREBASE_URL
) -> Union[str, List[str]]:
    bucket_name, path = parse_url(blob.public_url)

    tokens: Union[str, List[str], None] = None
    if url_type == UrlType.FIREBASE_URL:
        tokens = get_access_token(blob)

    if tokens is None:
        return _get_download_url(bucket_name=bucket_name, path=path, token=None, url_type=url_type)
    elif type(tokens) is str:
        return _get_download_url(
            bucket_name=bucket_name, path=path, token=tokens, url_type=url_type
        )
    elif isinstance(tokens, list):
        return list(
            map(
                lambda token: _get_download_url(
                    bucket_name=bucket_name, path=path, token=token, url_type=url_type
                ),
                tokens,
            )
        )
    else:
        raise ValueError("Logic error.")


def estimate_download_url(
    bucket_name: str,
    path: str,
    access_tokens: Union[str, List[str]],
    url_type: UrlType = UrlType.FIREBASE_URL,
) -> Union[str, List[str]]:
    if type(access_tokens) is str:
        return _get_download_url(url_type, bucket_name, path, access_tokens)
    elif isinstance(access_tokens, list):
        return list(
            map(
                lambda access_token: _get_download_url(url_type, bucket_name, path, access_token),
                access_tokens,
            )
        )

    raise ValueError("Logic error.")


def get_gs_path(blob: Blob) -> str:
    bucket_name, path = parse_url(blob.public_url)

    return f"gs://{bucket_name}/{path}"


# ---------- private ----------


def _get_download_url(url_type: UrlType, bucket_name: str, path: str, token: Optional[str]) -> str:
    assert url_type != UrlType.FIREBASE_URL or (
        url_type == UrlType.FIREBASE_URL and token is not None
    )

    if url_type == UrlType.PUBLIC_URL:
        encoded_path = quote(path)
        return f"https://storage.googleapis.com/{bucket_name}/{encoded_path}"
    elif url_type == UrlType.AUTHENTICATED_URL:
        encoded_path = quote(path)
        return f"https://storage.cloud.google.com/{bucket_name}/{encoded_path}"
    elif url_type == UrlType.FIREBASE_URL:
        encoded_path = quote(path, safe="")
        return f"https://firebasestorage.googleapis.com/v0/b/{bucket_name}/o/{encoded_path}?alt=media&token={token}"

    raise Exception("Logic error.")
