from typing import Optional

from google.cloud.storage import Blob, Client

from csfutils._client import parse_url


def get_blob_from_server(blob: Blob, force: bool, client: Optional[Client]) -> Optional[Blob]:
    # short
    if not force and blob.size is not None:
        return blob

    use_client = client if client is not None else blob.client
    bucket_name, path = parse_url(blob.public_url)

    return use_client.bucket(bucket_name).get_blob(path)
