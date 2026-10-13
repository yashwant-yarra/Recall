from datetime import timedelta

from google.auth.transport.requests import Request

from .config import settings


def sign_upload_url(
    bucket, credentials, gcs_path: str, content_type: str, size_bytes: int
) -> tuple[str, dict[str, str]]:
    """Signs via IAM signBlob (email + token) so it works on Cloud Run without a key file."""
    if not credentials.valid:
        credentials.refresh(Request())
    # Exact-size range: GCS rejects any upload whose length differs from what the client declared.
    headers = {
        "x-goog-content-length-range": f"{size_bytes},{size_bytes}",
        "x-goog-if-generation-match": "0",
    }

    url = bucket.blob(gcs_path).generate_signed_url(
        version="v4",
        expiration=timedelta(seconds=settings.upload_url_ttl_seconds),
        method="PUT",
        content_type=content_type,
        service_account_email=credentials.service_account_email,
        access_token=credentials.token,
        # The library adds "Host" to the dict it receives, so pass a copy.
        headers=dict(headers),
    )
    return url, {**headers, "Content-Type": content_type}
