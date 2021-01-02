from typing import Optional
import uuid

from google.cloud.storage import Blob
from google.cloud.storage.blob import Blob
from testconfig import TEST_ARG

from csfutils import (
    add_access_token,
    delete_access_token,
    get_access_token,
    init_storage,
    upload_from_filename_for_firebase,
)


class TestAccessToken(object):
    def _get_path(self, child: Optional[str]) -> str:
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

    # ---------- add ----------

    def test_add_access_token_0_to_1(self):
        # upload empty access token
        blob = self._blob("📔file📓.txt")
        blob.upload_from_filename("./test_resources/📔file📓.txt")

        # add
        expected_access_token = str(uuid.uuid4())
        _ = add_access_token(blob, expected_access_token)

        actual_access_token = get_access_token(blob)

        assert type(actual_access_token) is str
        assert actual_access_token == expected_access_token

    def test_add_access_token_1_to_2(self):
        blob = self._blob("📔file📓.txt")

        # upload with access token
        expected_access_token_1 = str(uuid.uuid4())
        _ = upload_from_filename_for_firebase(
            blob, "./test_resources/📔file📓.txt", expected_access_token_1
        )

        # add access token
        expected_access_token_2 = str(uuid.uuid4())
        _ = add_access_token(blob, expected_access_token_2)

        actual_access_tokens = get_access_token(blob)

        expected_access_tokens = [expected_access_token_1, expected_access_token_2]

        assert isinstance(actual_access_tokens, list)
        assert actual_access_tokens == expected_access_tokens

    # ---------- get ----------

    def test_get_access_token_0(self):
        # upload empty access token
        blob = self._blob("📔file📓.txt")
        blob.upload_from_filename("./test_resources/📔file📓.txt")

        access_token = get_access_token(blob)

        assert access_token is None

    def test_get_access_token_1(self):
        # upload with access token
        blob = self._blob("📔file📓.txt")
        expected_access_token = str(uuid.uuid4())
        _ = upload_from_filename_for_firebase(
            blob, "./test_resources/📔file📓.txt", expected_access_token
        )

        access_token = get_access_token(blob)

        assert access_token == expected_access_token

    def test_get_access_token_2(self):
        blob = self._blob("📔file📓.txt")

        # upload with access token
        expected_access_token_1 = str(uuid.uuid4())
        _ = upload_from_filename_for_firebase(
            blob, "./test_resources/📔file📓.txt", expected_access_token_1
        )

        new_blob_with_1_access_token = self._get_blob("📔file📓.txt")
        assert new_blob_with_1_access_token is not None
        assert get_access_token(new_blob_with_1_access_token) == expected_access_token_1

        # add access token
        expected_access_token_2 = str(uuid.uuid4())
        _ = add_access_token(blob, expected_access_token_2)

        # actual_access_tokens returns str if get_access_token has bug.
        actual_access_tokens = get_access_token(new_blob_with_1_access_token)

        expected_access_tokens = [expected_access_token_1, expected_access_token_2]

        assert isinstance(actual_access_tokens, list)
        assert actual_access_tokens == expected_access_tokens

    # ---------- delete ----------

    def test_delete_access_token_2_to_1(self):
        blob = self._blob("📔file📓.txt")

        # upload with access token
        expected_access_token_1 = str(uuid.uuid4())
        _ = upload_from_filename_for_firebase(
            blob, "./test_resources/📔file📓.txt", expected_access_token_1
        )

        # add access token
        expected_access_token_2 = str(uuid.uuid4())
        _ = add_access_token(blob, expected_access_token_2)

        delete_access_token(blob, expected_access_token_1)

        assert get_access_token(blob) == expected_access_token_2

    def test_delete_access_token_1_to_0(self):
        blob = self._blob("📔file📓.txt")

        # upload with access token
        expected_access_token_1 = str(uuid.uuid4())
        _ = upload_from_filename_for_firebase(
            blob, "./test_resources/📔file📓.txt", expected_access_token_1
        )

        delete_access_token(blob, expected_access_token_1)

        assert get_access_token(blob) is None

    def test_delete_access_token_0(self):
        blob = self._blob("📔file📓.txt")
        blob.upload_from_filename("./test_resources/📔file📓.txt")

        delete_access_token(blob, "aaa")

        assert get_access_token(blob) is None

    def test_delete_access_token_multiple(self):
        blob = self._blob("📔file📓.txt")

        # upload with access token
        expected_access_token_1 = str(uuid.uuid4())
        _ = upload_from_filename_for_firebase(
            blob, "./test_resources/📔file📓.txt", expected_access_token_1
        )

        # add access token
        expected_access_token_2 = str(uuid.uuid4())
        _ = add_access_token(blob, expected_access_token_2)

        tokens = [expected_access_token_1, expected_access_token_2]

        delete_access_token(blob, tokens)

        assert get_access_token(blob) is None
