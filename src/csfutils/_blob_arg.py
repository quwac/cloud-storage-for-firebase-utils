class BlobArg(object):
    bucket_name: str
    path: str

    def __init__(self, bucket_name: str, path: str):
        self.bucket_name = bucket_name
        self.path = path

    def __repr__(self) -> str:
        return f"BlobArg(bucket_name={self.bucket_name},path={self.path})"
