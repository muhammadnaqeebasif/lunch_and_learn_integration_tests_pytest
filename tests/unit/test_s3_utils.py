import pytest

from lunch_and_learn.s3_utils import InvalidS3URIError, split_s3_uri


@pytest.mark.parametrize(
    "s3_uri,expected_s3_bucket,expected_s3_key",
    [
        ("s3://fake_bucket/fake_folder/", "fake_bucket", "fake_folder/"),
        ("s3://fake_bucket/fake_folder/fake_file.json", "fake_bucket", "fake_folder/fake_file.json"),
    ],
)
def test_split_uri(s3_uri: str, expected_s3_bucket: str, expected_s3_key: str) -> None:
    actual_bucket, actual_s3_key = split_s3_uri(s3_uri)
    assert actual_bucket == expected_s3_bucket
    assert actual_s3_key == expected_s3_key


@pytest.mark.parametrize("s3_uri", [("s3:/fake_bucket/"), ("s3:///fake_folder")])
def test_split_s3_uri_invalid_uri(s3_uri: str) -> None:
    with pytest.raises(InvalidS3URIError):
        split_s3_uri(s3_uri=s3_uri)
