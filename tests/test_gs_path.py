from testconfig import TEST_ARG

from csfutils import get_gs_path, init_storage


class TestGsPath(object):
    def test_gs_path(self):
        storage = init_storage(TEST_ARG.service_account_json_path)

        bucket_name = TEST_ARG.bucket_name
        blob = storage.bucket(bucket_name).blob("item1/item2/item3/file😊.txt")

        actual_gs_path = get_gs_path(blob)
        expected_gs_path = f"gs://{bucket_name}/item1/item2/item3/file😊.txt"

        assert actual_gs_path == expected_gs_path
