import copy
import json
import re
from typing import Any, Dict, List, Optional, Union
import uuid

from google.api_core.exceptions import InvalidArgument
from google.cloud.storage import Blob, Client

from csfutils._const import TOKENS_KEY
from csfutils._utils import get_blob_from_server

_UUID_PATTERN = re.compile(
    r"[0-9a-fA-F]{8}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{12}"  # noqa: FS003
)

# ---------- public ----------


def add_access_token(
    blob: Blob, access_token: Optional[str] = None, client: Optional[Client] = None
) -> str:
    return add_access_token_impl(blob, access_token, None, client)


def validate_access_token(access_token: str):
    if _UUID_PATTERN.match(access_token) is None:
        raise InvalidArgument(f"Access token invalid. access_token={access_token}")


def get_access_token(blob: Blob, client: Optional[Client] = None) -> Union[str, List[str], None]:
    try:
        server_blob = get_blob_from_server(blob, True, client)
        if server_blob is None:
            raise ValueError("Cannot get server_blob.")
        tokens = _get_access_tokens(server_blob)
        if len(tokens) == 1:
            return tokens[0]
        else:
            return tokens
    except:
        return None


def delete_access_token(
    blob: Blob, access_tokens: Union[str, List[str]], client: Optional[Client] = None
):
    if type(access_tokens) is str:
        access_tokens = [access_tokens]
    assert isinstance(access_tokens, list)
    if len(access_tokens) == 0:
        return

    server_blob = get_blob_from_server(blob, True, client)
    if server_blob is None:
        raise ValueError("Blob cannot get from server.")

    try:
        old_tokens = _get_access_tokens(server_blob)
    except:
        return

    new_tokens: List[str] = []
    for token in old_tokens:
        if token not in access_tokens:
            new_tokens.append(token)

    if old_tokens == new_tokens:
        return

    new_tokens_len = len(new_tokens)
    if new_tokens_len == 0:
        _delete_metadata(server_blob, TOKENS_KEY, client)
    else:
        tokens_str = ",".join(new_tokens)
        _merge_metadata(
            blob=server_blob,
            metadata_diff={TOKENS_KEY: tokens_str},
            content_disposition=None,
            client=client,
        )


def generate_access_token() -> str:
    return str(uuid.uuid4())


# ---------- private ----------


def _error(metadata: Any) -> ValueError:
    return ValueError(
        f"""get_download_url error.
        * You might obtain blob from Bucket.blob() instead of Bucket.get_blob().
        * /{TOKENS_KEY} may not found or illegal value like empty. metadata={json.dumps(metadata, ensure_ascii=False)}
        """
    )


def add_access_token_impl(
    blob: Blob,
    access_token: Optional[str],
    content_disposition: Optional[str],
    client: Optional[Client],
) -> str:
    if access_token is None:
        access_token = generate_access_token()
    validate_access_token(access_token)

    server_blob = get_blob_from_server(blob, True, client)
    if server_blob is None:
        raise ValueError("Blob cannot get from server.")

    try:
        old_tokens = _get_access_tokens(server_blob)
    except:
        old_tokens = []

    new_tokens: List[str] = copy.deepcopy(old_tokens)
    new_tokens.append(access_token)
    tokens_str = ",".join(new_tokens)

    _merge_metadata(
        blob=blob,
        metadata_diff={TOKENS_KEY: tokens_str},
        content_disposition=content_disposition,
        client=client,
    )

    return access_token


def _get_access_tokens(blob: Blob) -> List[str]:
    metadata = blob.metadata

    if metadata is None or TOKENS_KEY not in metadata:
        raise _error(metadata)

    token_or_tokens: str = metadata[TOKENS_KEY]
    if token_or_tokens == "":
        raise _error(metadata)

    if "," in token_or_tokens:
        tokens = token_or_tokens.split(",")
    else:
        tokens = [token_or_tokens]

    assert len(tokens) > 0
    return tokens


def _merge_metadata(
    blob: Blob,
    metadata_diff: Dict[str, Any],
    content_disposition: Optional[str],
    client: Optional[Client],
):
    # metadata
    old_metadata: Optional[Dict[str, Any]] = blob.metadata
    if old_metadata is None:
        old_metadata = {}

    new_metadata = dict(old_metadata, **metadata_diff)

    blob.metadata = new_metadata

    # content disposition
    if content_disposition is not None:
        blob.content_disposition = content_disposition

    blob.patch(client=client)


def _delete_metadata(blob: Blob, key: str, client: Optional[Client]):
    old_metadata = blob.metadata
    if old_metadata is None:
        return

    new_metadata = copy.deepcopy(old_metadata)
    new_metadata[key] = ""

    blob.metadata = new_metadata
    blob.patch(client=client)
