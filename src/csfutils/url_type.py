from enum import Enum


class UrlType(Enum):
    """Cloud Storage URL type.

    * PUBLIC_URL: https://storage.googleapis.com
    * AUTHENTICATED_URL: https://storage.cloud.google.com
    * FIREBASE_URL: https://firebasestorage.googleapis.com
    """

    PUBLIC_URL = (1,)
    AUTHENTICATED_URL = (2,)
    FIREBASE_URL = 3
