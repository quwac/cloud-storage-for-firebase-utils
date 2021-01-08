from testconfig import TEST_ARG

from csfutils import estimate_download_url, generate_access_token


class TestGetDownloadUrl(object):
    def test_estimate_download_url_public_url(self):
        bucket_name = TEST_ARG.bucket_name
        path = "item1/item2/item3/file😊.txt"
        access_token = "3cdc56f7-5319-4dfc-b0d4-333ffbbf08be"

        actual_url = estimate_download_url(bucket_name, path, access_token)
        expected_url = f"https://firebasestorage.googleapis.com/v0/b/{bucket_name}/o/item1%2Fitem2%2Fitem3%2Ffile%F0%9F%98%8A.txt?alt=media&token=3cdc56f7-5319-4dfc-b0d4-333ffbbf08be"

        assert actual_url == expected_url
