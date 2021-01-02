"""
This type stub file was generated by pyright.
"""

import collections
import datetime
import six

"""
This type stub file was generated by pyright.
"""
NOW = datetime.datetime.utcnow
SERVICE_ACCOUNT_URL = "https://googleapis.dev/python/google-api-core/latest/" "auth.html#setting-up-a-service-account"
def ensure_signed_credentials(credentials):
    """Raise AttributeError if the credentials are unsigned.

    :type credentials: :class:`google.auth.credentials.Signing`
    :param credentials: The credentials used to create a private key
                        for signing text.

    :raises: :exc:`AttributeError` if credentials is not an instance
            of :class:`google.auth.credentials.Signing`.
    """
    ...

def get_signed_query_params_v2(credentials, expiration, string_to_sign):
    """Gets query parameters for creating a signed URL.

    :type credentials: :class:`google.auth.credentials.Signing`
    :param credentials: The credentials used to create a private key
                        for signing text.

    :type expiration: int or long
    :param expiration: When the signed URL should expire.

    :type string_to_sign: str
    :param string_to_sign: The string to be signed by the credentials.

    :raises: :exc:`AttributeError` if credentials is not an instance
            of :class:`google.auth.credentials.Signing`.

    :rtype: dict
    :returns: Query parameters matching the signing credentials with a
              signed payload.
    """
    ...

def get_expiration_seconds_v2(expiration):
    """Convert 'expiration' to a number of seconds in the future.

    :type expiration: Union[Integer, datetime.datetime, datetime.timedelta]
    :param expiration: Point in time when the signed URL should expire. If
                       a ``datetime`` instance is passed without an explicit
                       ``tzinfo`` set,  it will be assumed to be ``UTC``.

    :raises: :exc:`TypeError` when expiration is not a valid type.

    :rtype: int
    :returns: a timestamp as an absolute number of seconds since epoch.
    """
    ...

_EXPIRATION_TYPES = six.integer_types + (datetime.datetime, datetime.timedelta)
def get_expiration_seconds_v4(expiration):
    """Convert 'expiration' to a number of seconds offset from the current time.

    :type expiration: Union[Integer, datetime.datetime, datetime.timedelta]
    :param expiration: Point in time when the signed URL should expire. If
                       a ``datetime`` instance is passed without an explicit
                       ``tzinfo`` set,  it will be assumed to be ``UTC``.

    :raises: :exc:`TypeError` when expiration is not a valid type.
    :raises: :exc:`ValueError` when expiration is too large.
    :rtype: Integer
    :returns: seconds in the future when the signed URL will expire
    """
    ...

def get_canonical_headers(headers):
    """Canonicalize headers for signing.

    See:
    https://cloud.google.com/storage/docs/access-control/signed-urls#about-canonical-extension-headers

    :type headers: Union[dict|List(Tuple(str,str))]
    :param headers:
        (Optional) Additional HTTP headers to be included as part of the
        signed URLs.  See:
        https://cloud.google.com/storage/docs/xml-api/reference-headers
        Requests using the signed URL *must* pass the specified header
        (name and value) with each request for the URL.

    :rtype: str
    :returns: List of headers, normalized / sortted per the URL refernced above.
    """
    ...

_Canonical = collections.namedtuple("_Canonical", ["method", "resource", "query_parameters", "headers"])
def canonicalize_v2(method, resource, query_parameters, headers):
    """Canonicalize method, resource per the V2 spec.

    :type method: str
    :param method: The HTTP verb that will be used when requesting the URL.
                   Defaults to ``'GET'``. If method is ``'RESUMABLE'`` then the
                   signature will additionally contain the `x-goog-resumable`
                   header, and the method changed to POST. See the signed URL
                   docs regarding this flow:
                   https://cloud.google.com/storage/docs/access-control/signed-urls

    :type resource: str
    :param resource: A pointer to a specific resource
                     (typically, ``/bucket-name/path/to/blob.txt``).

    :type query_parameters: dict
    :param query_parameters:
        (Optional) Additional query parameters to be included as part of the
        signed URLs.  See:
        https://cloud.google.com/storage/docs/xml-api/reference-headers#query

    :type headers: Union[dict|List(Tuple(str,str))]
    :param headers:
        (Optional) Additional HTTP headers to be included as part of the
        signed URLs.  See:
        https://cloud.google.com/storage/docs/xml-api/reference-headers
        Requests using the signed URL *must* pass the specified header
        (name and value) with each request for the URL.

    :rtype: :class:_Canonical
    :returns: Canonical method, resource, query_parameters, and headers.
    """
    ...

def generate_signed_url_v2(credentials, resource, expiration, api_access_endpoint=..., method=..., content_md5=..., content_type=..., response_type=..., response_disposition=..., generation=..., headers=..., query_parameters=..., service_account_email=..., access_token=...):
    """Generate a V2 signed URL to provide query-string auth'n to a resource.

    .. note::

        Assumes ``credentials`` implements the
        :class:`google.auth.credentials.Signing` interface. Also assumes
        ``credentials`` has a ``service_account_email`` property which
        identifies the credentials.

    .. note::

        If you are on Google Compute Engine, you can't generate a signed URL.
        Follow `Issue 922`_ for updates on this. If you'd like to be able to
        generate a signed URL from GCE, you can use a standard service account
        from a JSON file rather than a GCE service account.

    See headers `reference`_ for more details on optional arguments.

    .. _Issue 922: https://github.com/GoogleCloudPlatform/\
                   google-cloud-python/issues/922
    .. _reference: https://cloud.google.com/storage/docs/reference-headers

    :type credentials: :class:`google.auth.credentials.Signing`
    :param credentials: Credentials object with an associated private key to
                        sign text.

    :type resource: str
    :param resource: A pointer to a specific resource
                     (typically, ``/bucket-name/path/to/blob.txt``).
                     Caller should have already URL-encoded the value.

    :type expiration: Union[Integer, datetime.datetime, datetime.timedelta]
    :param expiration: Point in time when the signed URL should expire. If
                       a ``datetime`` instance is passed without an explicit
                       ``tzinfo`` set,  it will be assumed to be ``UTC``.

    :type api_access_endpoint: str
    :param api_access_endpoint: (Optional) URI base. Defaults to empty string.

    :type method: str
    :param method: The HTTP verb that will be used when requesting the URL.
                   Defaults to ``'GET'``. If method is ``'RESUMABLE'`` then the
                   signature will additionally contain the `x-goog-resumable`
                   header, and the method changed to POST. See the signed URL
                   docs regarding this flow:
                   https://cloud.google.com/storage/docs/access-control/signed-urls


    :type content_md5: str
    :param content_md5: (Optional) The MD5 hash of the object referenced by
                        ``resource``.

    :type content_type: str
    :param content_type: (Optional) The content type of the object referenced
                         by ``resource``.

    :type response_type: str
    :param response_type: (Optional) Content type of responses to requests for
                          the signed URL. Ignored if content_type is set on
                          object/blob metadata.

    :type response_disposition: str
    :param response_disposition: (Optional) Content disposition of responses to
                                 requests for the signed URL.

    :type generation: str
    :param generation: (Optional) A value that indicates which generation of
                       the resource to fetch.

    :type headers: Union[dict|List(Tuple(str,str))]
    :param headers:
        (Optional) Additional HTTP headers to be included as part of the
        signed URLs.  See:
        https://cloud.google.com/storage/docs/xml-api/reference-headers
        Requests using the signed URL *must* pass the specified header
        (name and value) with each request for the URL.

    :type service_account_email: str
    :param service_account_email: (Optional) E-mail address of the service account.

    :type access_token: str
    :param access_token: (Optional) Access token for a service account.

    :type query_parameters: dict
    :param query_parameters:
        (Optional) Additional query parameters to be included as part of the
        signed URLs.  See:
        https://cloud.google.com/storage/docs/xml-api/reference-headers#query

    :raises: :exc:`TypeError` when expiration is not a valid type.
    :raises: :exc:`AttributeError` if credentials is not an instance
            of :class:`google.auth.credentials.Signing`.

    :rtype: str
    :returns: A signed URL you can use to access the resource
              until expiration.
    """
    ...

SEVEN_DAYS = 7 * 24 * 60 * 60
DEFAULT_ENDPOINT = "https://storage.googleapis.com"
def generate_signed_url_v4(credentials, resource, expiration, api_access_endpoint=..., method=..., content_md5=..., content_type=..., response_type=..., response_disposition=..., generation=..., headers=..., query_parameters=..., service_account_email=..., access_token=..., _request_timestamp=...):
    """Generate a V4 signed URL to provide query-string auth'n to a resource.

    .. note::

        Assumes ``credentials`` implements the
        :class:`google.auth.credentials.Signing` interface. Also assumes
        ``credentials`` has a ``service_account_email`` property which
        identifies the credentials.

    .. note::

        If you are on Google Compute Engine, you can't generate a signed URL.
        Follow `Issue 922`_ for updates on this. If you'd like to be able to
        generate a signed URL from GCE, you can use a standard service account
        from a JSON file rather than a GCE service account.

    See headers `reference`_ for more details on optional arguments.

    .. _Issue 922: https://github.com/GoogleCloudPlatform/\
                   google-cloud-python/issues/922
    .. _reference: https://cloud.google.com/storage/docs/reference-headers

    :type credentials: :class:`google.auth.credentials.Signing`
    :param credentials: Credentials object with an associated private key to
                        sign text.

    :type resource: str
    :param resource: A pointer to a specific resource
                     (typically, ``/bucket-name/path/to/blob.txt``).
                     Caller should have already URL-encoded the value.

    :type expiration: Union[Integer, datetime.datetime, datetime.timedelta]
    :param expiration: Point in time when the signed URL should expire. If
                       a ``datetime`` instance is passed without an explicit
                       ``tzinfo`` set,  it will be assumed to be ``UTC``.

    :type api_access_endpoint: str
    :param api_access_endpoint: (Optional) URI base. Defaults to
                                "https://storage.googleapis.com/"

    :type method: str
    :param method: The HTTP verb that will be used when requesting the URL.
                   Defaults to ``'GET'``. If method is ``'RESUMABLE'`` then the
                   signature will additionally contain the `x-goog-resumable`
                   header, and the method changed to POST. See the signed URL
                   docs regarding this flow:
                   https://cloud.google.com/storage/docs/access-control/signed-urls


    :type content_md5: str
    :param content_md5: (Optional) The MD5 hash of the object referenced by
                        ``resource``.

    :type content_type: str
    :param content_type: (Optional) The content type of the object referenced
                         by ``resource``.

    :type response_type: str
    :param response_type: (Optional) Content type of responses to requests for
                          the signed URL. Ignored if content_type is set on
                          object/blob metadata.

    :type response_disposition: str
    :param response_disposition: (Optional) Content disposition of responses to
                                 requests for the signed URL.

    :type generation: str
    :param generation: (Optional) A value that indicates which generation of
                       the resource to fetch.

    :type headers: dict
    :param headers:
        (Optional) Additional HTTP headers to be included as part of the
        signed URLs.  See:
        https://cloud.google.com/storage/docs/xml-api/reference-headers
        Requests using the signed URL *must* pass the specified header
        (name and value) with each request for the URL.

    :type query_parameters: dict
    :param query_parameters:
        (Optional) Additional query parameters to be included as part of the
        signed URLs.  See:
        https://cloud.google.com/storage/docs/xml-api/reference-headers#query

    :type service_account_email: str
    :param service_account_email: (Optional) E-mail address of the service account.

    :type access_token: str
    :param access_token: (Optional) Access token for a service account.

    :raises: :exc:`TypeError` when expiration is not a valid type.
    :raises: :exc:`AttributeError` if credentials is not an instance
            of :class:`google.auth.credentials.Signing`.

    :rtype: str
    :returns: A signed URL you can use to access the resource
              until expiration.
    """
    ...

def get_v4_now_dtstamps():
    """Get current timestamp and datestamp in V4 valid format.

    :rtype: str, str
    :returns: Current timestamp, datestamp.
    """
    ...

