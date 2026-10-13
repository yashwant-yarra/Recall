from datetime import timedelta
from google.auth.transport.requests import Request

from .config import settings


def sign_upload_url(bucket, credentials, gcs_path: str, content_type: str) -> str:
    """
    Generate a signed URL for uploading a file to Google Cloud Storage.

    Args:
        bucket: The GCS bucket object.
        credentials: The credentials for signing the URL.
        gcs_path (str): The path in the GCS bucket where the file will be uploaded.
        content_type (str): The content type of the file being uploaded.

    Returns:
        str: The signed upload URL.
    """

    if not credentials.valid:
        credentials.refresh(Request())
    expiration=timedelta(seconds=settings.upload_url_ttl_seconds)
    headers={"x-goog-content-length-range": f"1,{settings.max_upload_size}"}

    url = bucket.blob(gcs_path).generate_signed_url(
        version="v4",
        expiration=expiration,
        method="PUT",
        content_type=content_type,
        service_account_email=credentials.service_account_email,
        access_token=credentials.token,
        headers=headers
    )
    return url