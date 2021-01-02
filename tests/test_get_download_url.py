import pytest
from testconfig import TEST_ARG

from csfutils import get_download_url, init_storage
from csfutils.url_type import UrlType


class TestGetDownloadUrl(object):
    def test_get_download_url_public_url(self):
        storage = init_storage(TEST_ARG.service_account_json_path)

        bucket_name = TEST_ARG.bucket_name
        blob = storage.bucket(bucket_name).blob("item1/item2/item3/file😊.txt")

        actual_url = get_download_url(blob, UrlType.PUBLIC_URL)
        assert isinstance(actual_url, str)

        expected_url = blob.public_url

        assert actual_url == expected_url

    def test_get_download_url_authenticated_url(self):
        storage = init_storage(TEST_ARG.service_account_json_path)

        bucket_name = TEST_ARG.bucket_name
        blob = storage.bucket(bucket_name).blob("item1/item2/item3/file😊.txt")

        actual_url = get_download_url(blob, UrlType.AUTHENTICATED_URL)
        assert isinstance(actual_url, str)

        expected_url = f"https://storage.cloud.google.com/{bucket_name}/item1/item2/item3/file%F0%9F%98%8A.txt"

        assert actual_url == expected_url

    def test_get_download_url_firebase_url(self):
        storage = init_storage(TEST_ARG.service_account_json_path)

        bucket_name = TEST_ARG.bucket_name
        #  Bucket.get_blob()
        blob = storage.bucket(bucket_name).get_blob("item1/item2/item3/file😊.txt")
        assert blob is not None

        actual_url = get_download_url(blob, UrlType.FIREBASE_URL)
        assert isinstance(actual_url, str)

        expected_url = f"https://firebasestorage.googleapis.com/v0/b/{bucket_name}/o/item1%2Fitem2%2Fitem3%2Ffile%F0%9F%98%8A.txt?alt=media&token=3cdc56f7-5319-4dfc-b0d4-333ffbbf08be"

        assert actual_url == expected_url

    def test_get_download_url_firebase_url_using_blob(self):
        storage = init_storage(TEST_ARG.service_account_json_path)

        bucket_name = TEST_ARG.bucket_name
        #  Bucket.blob()
        blob = storage.bucket(bucket_name).blob("item1/item2/item3/file😊.txt")

        actual_url = get_download_url(blob, UrlType.FIREBASE_URL)
        assert isinstance(actual_url, str)

        expected_url = f"https://firebasestorage.googleapis.com/v0/b/{bucket_name}/o/item1%2Fitem2%2Fitem3%2Ffile%F0%9F%98%8A.txt?alt=media&token=3cdc56f7-5319-4dfc-b0d4-333ffbbf08be"

        assert actual_url == expected_url

    def test_get_download_url_firebase_url_multiple(self):
        storage = init_storage(TEST_ARG.service_account_json_path)

        bucket_name = TEST_ARG.bucket_name
        blob = storage.bucket(bucket_name).get_blob(
            "item1/item2/item3/multiple_access_tokens🎫🎫🎫.txt"
        )
        assert blob is not None

        actual_urls = get_download_url(blob, UrlType.FIREBASE_URL)
        print(f"actual_urls={actual_urls}")
        assert isinstance(actual_urls, list)

        expected_urls = [
            f"https://firebasestorage.googleapis.com/v0/b/{bucket_name}/o/item1%2Fitem2%2Fitem3%2Fmultiple_access_tokens%F0%9F%8E%AB%F0%9F%8E%AB%F0%9F%8E%AB.txt?alt=media&token=dcec53ef-bc29-4568-bc59-ad4e1e91b825",
            f"https://firebasestorage.googleapis.com/v0/b/{bucket_name}/o/item1%2Fitem2%2Fitem3%2Fmultiple_access_tokens%F0%9F%8E%AB%F0%9F%8E%AB%F0%9F%8E%AB.txt?alt=media&token=b4cdfeda-94e8-4047-9b9e-cb5baaa3966a",
            f"https://firebasestorage.googleapis.com/v0/b/{bucket_name}/o/item1%2Fitem2%2Fitem3%2Fmultiple_access_tokens%F0%9F%8E%AB%F0%9F%8E%AB%F0%9F%8E%AB.txt?alt=media&token=ead34b33-d957-49a8-ad6f-0b8282acf49c",
        ]
        assert sorted(actual_urls) == sorted(expected_urls)

    def test_get_download_url_firebase_url_error_by_no_access_token(self):
        storage = init_storage(TEST_ARG.service_account_json_path)

        bucket_name = TEST_ARG.bucket_name
        blob = storage.bucket(bucket_name).get_blob("item1/item2/item3/no_access_token👿.txt")
        assert blob is not None

        with pytest.raises(Exception):  # type: ignore
            _ = get_download_url(blob, UrlType.FIREBASE_URL)
