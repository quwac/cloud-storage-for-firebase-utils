from typing import Optional
import uuid

from google.cloud.storage import Blob, Client
import pytest
from testconfig import TEST_ARG

from csfutils import (
    get_access_token,
    init_storage,
    ref_from_url,
    upload_from_file_for_firebase,
    upload_from_filename_for_firebase,
    upload_from_string_for_firebase,
)


class TestUploadForFirebase(object):
    def _get_path(self, child: Optional[str]):
        if child is not None:
            path = f"upload/item1/item2/{child}"
        else:
            path = "upload/item1/item2"

        return path

    def _blob(self, child: Optional[str]) -> Blob:
        storage = init_storage(TEST_ARG.service_account_json_path)
        return storage.bucket(TEST_ARG.bucket_name).blob(self._get_path(child))

    def _get_blob(self, child: Optional[str]) -> Optional[Blob]:
        storage = init_storage(TEST_ARG.service_account_json_path)
        return storage.bucket(TEST_ARG.bucket_name).get_blob(self._get_path(child))

    def _delete_file(self):
        blob = self._get_blob("📔file📓.txt")
        if blob is not None:
            blob.delete()

    def setup_method(self):
        self._delete_file()

    def teardown_method(self):
        self._delete_file()

    def _check(self, client: Client, url: str):
        blob = ref_from_url(client, url)
        assert blob.exists()
        assert type(get_access_token(blob)) is str
        assert (
            blob.content_disposition == "inline; filename*=utf-8''%F0%9F%93%94file%F0%9F%93%93.txt"
        )

    # ========== file ==========

    def test_upload_from_file_for_firebase(self):
        blob = self._blob("📔file📓.txt")

        with open("./test_resources/📔file📓.txt") as f:
            url = upload_from_file_for_firebase(blob, f)

        self._check(blob.client, url)

    def test_upload_from_file_for_firebase_access_token(self):
        blob = self._blob("📔file📓.txt")

        with open("./test_resources/📔file📓.txt") as f:
            expected_access_token = str(uuid.uuid4())
            url = upload_from_file_for_firebase(blob, f, expected_access_token)

        self._check(blob.client, url)
        assert get_access_token(blob) == expected_access_token

    def test_upload_from_file_for_firebase_error_illegal_access_token(self):
        blob = self._blob("📔file📓.txt")

        with pytest.raises(Exception):
            with open("./test_resources/📔file📓.txt") as f:
                expected_access_token = "aaa"
                _ = upload_from_file_for_firebase(blob, f, expected_access_token)

        assert self._get_blob("📔file📓.txt") is None
        assert get_access_token(blob) is None

    # ========== filename ==========

    def test_upload_from_filename_for_firebase(self):
        blob = self._blob("📔file📓.txt")

        url = upload_from_filename_for_firebase(blob, "./test_resources/📔file📓.txt")

        self._check(blob.client, url)

    def test_upload_from_filename_for_firebase_access_token(self):
        blob = self._blob("📔file📓.txt")

        expected_access_token = str(uuid.uuid4())
        url = upload_from_filename_for_firebase(
            blob, "./test_resources/📔file📓.txt", expected_access_token
        )

        self._check(blob.client, url)
        assert get_access_token(blob) == expected_access_token

    def test_upload_from_filename_for_firebase_error_illegal_access_token(self):
        blob = self._blob("📔file📓.txt")

        with pytest.raises(Exception):
            expected_access_token = "aaa"
            _ = upload_from_filename_for_firebase(
                blob, "./test_resources/📔file📓.txt", expected_access_token
            )

        assert self._get_blob("📔file📓.txt") is None
        assert get_access_token(blob) is None

    # ========== string ==========

    def test_upload_from_string_for_firebase(self):
        blob = self._blob("📔file📓.txt")

        url = upload_from_string_for_firebase(blob, "string")

        self._check(blob.client, url)

    def test_upload_from_string_for_firebase_access_token(self):
        blob = self._blob("📔file📓.txt")

        expected_access_token = str(uuid.uuid4())
        url = upload_from_string_for_firebase(blob, "string", expected_access_token)

        self._check(blob.client, url)
        assert get_access_token(blob) == expected_access_token

    def test_upload_from_string_for_firebase_error_illegal_access_token(self):
        blob = self._blob("📔file📓.txt")

        with pytest.raises(Exception):
            expected_access_token = "aaa"
            _ = upload_from_string_for_firebase(blob, "string", expected_access_token)

        assert self._get_blob("📔file📓.txt") is None
        assert get_access_token(blob) is None
