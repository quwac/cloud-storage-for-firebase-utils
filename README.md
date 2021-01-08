# cloud-storage-for-firebase-utils

[![PyPI version](https://badge.fury.io/py/csfutils.svg)](https://badge.fury.io/py/csfutils) [![Python Versions](https://img.shields.io/pypi/pyversions/csfutils.svg)](https://pypi.org/project/csfutils/)
![lint & test](https://github.com/quwac/cloud-storage-for-firebase-utils/workflows/lint%20&%20test/badge.svg) [![codecov](https://codecov.io/gh/quwac/cloud-storage-for-firebase-utils/branch/main/graph/badge.svg)](https://codecov.io/gh/quwac/cloud-storage-for-firebase-utils)

Python utility for Cloud Storage for Firebase.

## What is This?

In order to use [Google Cloud Storage](https://cloud.google.com/storage?hl=en) with the [Firebase](https://firebase.google.com/docs/storage?hl=en) framework, you have to:

* Give an access token to uploaded files,
* Publish a URL with an access token for the domain `firebasestorage.googleapis.com`.
* As a further application, you may want to grant a new access token, remove an existing access token, or in a real use case, get a `google.cloud.storage.Blob` instance from a URL.

Unfortunately [google-cloud-storage](https://pypi.org/project/google-cloud-storage/) package does not provide the functions for them.

But by using **cloud-storage-for-firebase-utils** you can easily achieve them👍.

## Requirements

* Python >= 3.6
* [google-cloud-storage](https://pypi.org/project/google-cloud-storage/) >= 1.35.0

## Quick Start

First, install by `pip intall csfutils` .
Second, prepare a target file `stars⭐.jpg` .
Finally, run below code❗

```python
from google.cloud.storage import Blob, Bucket, Client

# Import package
# ==============
import csfutils

# Initialize google.cloud.storage.Client, Bucket and Blob instances
# =================================================================
storage: Client = Client()
bucket: Bucket = storage.bucket("example-project.appspot.com")  # PUT YOUR BUCKET NAME
blob: Blob = bucket.blob("images/stars⭐.jpg")  # PUT PATH ON CLOUD STORAGE YOU WANT

# 🔥Upload "./stars⭐.jpg" to Cloud Storage for Firebase
# ======================================================
uploaded_url: str = csfutils.upload_from_filename_for_firebase(blob, "./stars⭐.jpg")
print(f"uploaded_url={uploaded_url}")
# --> uploaded_url=https://firebasestorage.googleapis.com/v0/b/example-project.appspot.com/o/images%2Fstars%E2%9C%A7.jpg?alt=media&token=f7d0815d-96f8-4907-b22c-70ad9e38d7ff

# csfutils.upload_from_file_for_firebase() and csfutils.upload_from_string_for_firebase() also exist.

# 🔥Add, get and delete an access token
# =====================================
current_access_token = csfutils.get_access_token(blob)
assert type(current_access_token) is str
print(f"current_access_token={current_access_token}")
# --> current_access_token=f7d0815d-96f8-4907-b22c-70ad9e38d7ff

new_access_token: str = csfutils.add_access_token(blob)
print(f"new_access_token={new_access_token}")
# --> new_access_token=e0d97b72-44c3-415d-8d88-1e3aeae2fc28

access_tokens = csfutils.get_access_token(blob)
assert isinstance(access_tokens, list)
print(f"access_tokens={access_tokens}")
# --> current_access_token=['f7d0815d-96f8-4907-b22c-70ad9e38d7ff','e0d97b72-44c3-415d-8d88-1e3aeae2fc28']

csfutils.delete_access_token(blob, new_access_token)
print(f"latest_access_token={csfutils.get_access_token(blob)}")
# --> latest_access_token=f7d0815d-96f8-4907-b22c-70ad9e38d7ff

# 🔥Get google.cloud.storage.Blob instance from URL
# =================================================
blob_ref_from_url: Blob = csfutils.ref_from_url(
    storage,
    "https://firebasestorage.googleapis.com/v0/b/example-project.appspot.com/o/images%2Fstars%E2%9C%A7.jpg?alt=media&token=f7d0815d-96f8-4907-b22c-70ad9e38d7ff"
)
# --> blob_ref_from_url == storage.bucket("example-project.appspot.com").get_blob("images/stars✧.jpg")

```

## Bonus Track

```python
from csfutils

# BONUS 1: Get google.cloud.storage.Client instance
# =================================================
storage: Client = csfutils.init_storage("./your_service_account.json")

# BONUS 2: Parse URL to bucket name & path
# ========================================
bucket_name, path = csfutils.parse_url("https://firebasestorage.googleapis.com/v0/b/example-project.appspot.com/o/images%2Fstars%E2%9C%A7.jpg?alt=media&token=f7d0815d-96f8-4907-b22c-70ad9e38d7ff")
print(f"bucket_name={bucket_name},path={path}")
# --> bucket_name=example-project.appspot.com,path=images/stars⭐.jpg

# BONUS 3: Get 3 URLs: firebasestorage.googleapis.com, storage.googleapis.com and storage.cloud.google.com
# ========================================================================================================
blob: Blob = storage.bucket(bucket_name).blob(path)

firestorage_url = csfutils.get_download_url(blob)
print(f"firestorage_url={firestorage_url}")
# --> firestorage_url=https://firebasestorage.googleapis.com/v0/b/example-project.appspot.com/o/images%2Fstars%E2%9C%A7.jpg?alt=media&token=f7d0815d-96f8-4907-b22c-70ad9e38d7ff

public_url = csfutils.get_download_url(blob, csfutils.UrlType.PUBLIC_URL)
print(f"public_url={public_url}")
# --> firestorage_url=https://storage.googleapis.com/example-project.appspot.com/images/stars%E2%9C%A7.jpg

authenticated_url = csfutils.get_download_url(blob, csfutils.UrlType.AUTHENTICATED_URL)
print(f"authenticated_url={authenticated_url}")
# --> authenticated_url=https://storage.cloud.google.com/example-project.appspot.com/images/stars%E2%9C%A7.jpg

# BONUS 4: Get GS path
# ====================
gs_path = csfutils.get_gs_path(blob)
print(f"gs_path={gs_path}")
# --> gs_path=gs://example-project.appspot.com/images/stars⭐.jpg

# BONUS 5: Generate access token on a local machine
# =================================================
access_token = csfutils.generate_access_token()
print(f"access_token={access_token}")
# --> access_token=736da983-4853-4f55-a763-14e9cf1eb4c5

# BONUS 6: Estimate download URL
# ==============================
estimated_ffirestorage_url = csfutils.estimate_download_url(bucket_name, path, access_token)
# --> firestorage_url=https://firebasestorage.googleapis.com/v0/b/example-project.appspot.com/o/images%2Fstars%E2%9C%A7.jpg?alt=media&token=f7d0815d-96f8-4907-b22c-70ad9e38d7ff

```

## License

MIT License
