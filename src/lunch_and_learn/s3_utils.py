from typing import Tuple

SLASH_LITERAL = "/"


def split_s3_uri(s3_uri: str) -> Tuple[str, str]:
    if not s3_uri.startswith("s3://"):
        raise InvalidS3URIError(f"Invalid S3 URI: {s3_uri}")

    bucket = s3_uri.split(SLASH_LITERAL)[2]
    if not bucket:
        raise InvalidS3URIError(f"Bucket name not specified in S3 URI: {s3_uri}")

    s3_key = SLASH_LITERAL.join(s3_uri.split(SLASH_LITERAL)[3:])
    return bucket, s3_key


class InvalidS3URIError(Exception):
    """Raise Generic Invalid S3 URI Exception."""
