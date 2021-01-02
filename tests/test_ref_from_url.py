import pytest
from testconfig import TEST_ARG

from csfutils import init_storage, ref_from_url


class TestRefFromUrl(object):
    def test_ref_from_url_public_url(self):
        storage = init_storage(TEST_ARG.service_account_json_path)

        bucket_name = TEST_ARG.bucket_name
        expected_blob = storage.bucket(bucket_name).blob("item1/item2/item3/file😊.txt")
        assert expected_blob is not None

        actual_blob = ref_from_url(
            storage,
            f"https://storage.googleapis.com/{bucket_name}/item1/item2/item3/file%F0%9F%98%8A.txt",
        )

        assert actual_blob.path == expected_blob.path

    def test_ref_from_url_authenticated_url(self):
        storage = init_storage(TEST_ARG.service_account_json_path)

        bucket_name = TEST_ARG.bucket_name
        expected_blob = storage.bucket(bucket_name).blob("item1/item2/item3/file😊.txt")
        assert expected_blob is not None

        actual_blob = ref_from_url(
            storage,
            f"https://storage.cloud.google.com/{bucket_name}/item1/item2/item3/file%F0%9F%98%8A.txt",
        )

        assert actual_blob.path == expected_blob.path

    def test_ref_from_url_firebase(self):
        storage = init_storage(TEST_ARG.service_account_json_path)

        bucket_name = TEST_ARG.bucket_name
        expected_blob = storage.bucket(bucket_name).blob("item1/item2/item3/file😊.txt")
        assert expected_blob is not None

        actual_blob = ref_from_url(
            storage,
            f"https://firebasestorage.googleapis.com/v0/b/{bucket_name}/o/item1%2Fitem2%2Fitem3%2Ffile%F0%9F%98%8A.txt?alt=media&token=3cdc56f7-5319-4dfc-b0d4-333ffbbf08be",
        )

        assert actual_blob.path == expected_blob.path

    def test_ref_from_url_gs(self):
        storage = init_storage(TEST_ARG.service_account_json_path)

        bucket_name = TEST_ARG.bucket_name
        expected_blob = storage.bucket(bucket_name).blob("item1/item2/item3/file😊.txt")
        assert expected_blob is not None

        actual_blob = ref_from_url(storage, f"gs://{bucket_name}/item1/item2/item3/file😊.txt")

        assert actual_blob.path == expected_blob.path

    def test_ref_from_url_error_not_url(self):
        storage = init_storage(TEST_ARG.service_account_json_path)

        with pytest.raises(Exception):  # type: ignore
            _ = ref_from_url(storage, "illegal_url")

    def test_ref_from_url_error_illegal_https(self):
        storage = init_storage(TEST_ARG.service_account_json_path)

        with pytest.raises(Exception):  # type: ignore
            _ = ref_from_url(storage, "https://aaa")

    def test_ref_from_url_error_illegal_gs(self):
        storage = init_storage(TEST_ARG.service_account_json_path)

        with pytest.raises(Exception):  # type: ignore
            _ = ref_from_url(storage, "gs://aaa")

    def test_ref_from_url_error_not_exist(self):
        storage = init_storage(TEST_ARG.service_account_json_path)

        bucket_name = TEST_ARG.bucket_name
        expected_blob = storage.bucket(bucket_name).blob("not_exist.txt")
        assert expected_blob is not None

        with pytest.raises(Exception):
            _ = ref_from_url(storage, f"gs://{bucket_name}/not_exist.txt")
