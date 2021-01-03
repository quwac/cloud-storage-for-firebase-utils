from pathlib import Path
from typing import BinaryIO, Optional, Tuple, Union
from urllib.parse import quote

from google.cloud.storage import Blob, Client

from csfutils._client import parse_url
from csfutils._const import DEFAULT_TIMEOUT
from csfutils.blob._access_token import add_access_token_impl, validate_access_token
from csfutils.blob._path import get_download_url
from csfutils.url_type import UrlType

# ----------- public -----------


def upload_from_filename_for_firebase(
    blob: Blob,
    filename: Union[str, Path],
    access_token: Optional[str] = None,
    url_type: UrlType = UrlType.FIREBASE_URL,
    content_type: Optional[str] = None,
    client: Optional[Client] = None,
    predefined_acl: Optional[str] = None,
    if_generation_match: Optional[int] = None,
    if_generation_not_match: Optional[int] = None,
    if_metageneration_match: Optional[int] = None,
    if_metageneration_not_match: Optional[int] = None,
    timeout: Union[float, Tuple[float, float]] = DEFAULT_TIMEOUT,
    checksum: Optional[str] = None,
) -> str:
    if access_token is not None:
        validate_access_token(access_token)

    # upload
    blob.upload_from_filename(
        filename=filename,
        content_type=content_type,
        client=client,
        predefined_acl=predefined_acl,
        if_generation_match=if_generation_match,
        if_generation_not_match=if_generation_not_match,
        if_metageneration_match=if_metageneration_match,
        if_metageneration_not_match=if_metageneration_not_match,
        timeout=timeout,
        checksum=checksum,
    )

    return _set_metadata_and_return_url(blob, access_token, url_type, client)


def upload_from_file_for_firebase(
    blob: Blob,
    file_obj: BinaryIO,
    access_token: Optional[str] = None,
    url_type: UrlType = UrlType.FIREBASE_URL,
    rewind: bool = False,
    size: Optional[int] = None,
    content_type: Optional[str] = None,
    num_retries: Optional[int] = None,
    client: Optional[Client] = None,
    predefined_acl: Optional[str] = None,
    if_generation_match: Optional[int] = None,
    if_generation_not_match: Optional[int] = None,
    if_metageneration_match: Optional[int] = None,
    if_metageneration_not_match: Optional[int] = None,
    timeout: Union[float, Tuple[float, float]] = DEFAULT_TIMEOUT,
    checksum: Optional[str] = None,
) -> str:
    if access_token is not None:
        validate_access_token(access_token)

    # upload
    blob.upload_from_file(
        file_obj=file_obj,
        rewind=rewind,
        size=size,
        content_type=content_type,
        num_retries=num_retries,
        client=client,
        predefined_acl=predefined_acl,
        if_generation_match=if_generation_match,
        if_generation_not_match=if_generation_not_match,
        if_metageneration_match=if_metageneration_match,
        if_metageneration_not_match=if_metageneration_not_match,
        timeout=timeout,
        checksum=checksum,
    )

    return _set_metadata_and_return_url(blob, access_token, url_type, client)


def upload_from_string_for_firebase(
    blob: Blob,
    data: str,
    access_token: Optional[str] = None,
    url_type: UrlType = UrlType.FIREBASE_URL,
    content_type: str = "text/plain",
    client: Optional[Client] = None,
    predefined_acl: Optional[str] = None,
    if_generation_match: Optional[int] = None,
    if_generation_not_match: Optional[int] = None,
    if_metageneration_match: Optional[int] = None,
    if_metageneration_not_match: Optional[int] = None,
    timeout: Union[float, Tuple[float, float]] = DEFAULT_TIMEOUT,
    checksum: Optional[str] = None,
) -> str:
    if access_token is not None:
        validate_access_token(access_token)

    # upload
    blob.upload_from_string(
        data=data,
        content_type=content_type,
        client=client,
        predefined_acl=predefined_acl,
        if_generation_match=if_generation_match,
        if_generation_not_match=if_generation_not_match,
        if_metageneration_match=if_metageneration_match,
        if_metageneration_not_match=if_metageneration_not_match,
        timeout=timeout,
        checksum=checksum,
    )

    return _set_metadata_and_return_url(blob, access_token, url_type, client)


# ----------- private -----------


def _set_metadata_and_return_url(
    blob: Blob, access_token: Optional[str], url_type: UrlType, client: Optional[Client]
) -> str:
    _, path = parse_url(blob.public_url)

    file_name = path.split("/")[-1]

    content_disposition = f"inline; filename*=utf-8''{quote(file_name)}"
    access_token = add_access_token_impl(
        blob=blob,
        access_token=access_token,
        content_disposition=content_disposition,
        client=client,
    )
    url = get_download_url(blob, url_type)
    assert type(url) is str
    return url
