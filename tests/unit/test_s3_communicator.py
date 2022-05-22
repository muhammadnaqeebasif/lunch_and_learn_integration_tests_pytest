import pytest
from mypy_boto3_s3 import S3Client

from lunch_and_learn.s3_communicator import (
    InvalidS3URIError,
    S3Communicator,
    split_s3_uri,
)

FAKE_S3_FOLDER_ONE = "fake_folder_1"
FAKE_S3_FOLDER_TWO = "fake_folder_2"
NUMBER_OF_OBJECTS_IN_EACH_FAKE_FOLDER = 2

fake_s3_folders = [FAKE_S3_FOLDER_ONE, FAKE_S3_FOLDER_TWO]


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


@pytest.fixture(autouse=True)
def initialise_fake_s3_folders(mocked_s3_client: S3Client, fake_bucket: str) -> None:
    for fake_folder in fake_s3_folders:
        for fake_object_number in range(NUMBER_OF_OBJECTS_IN_EACH_FAKE_FOLDER):
            fake_key = f"{fake_folder}/fake_file_{fake_object_number}.txt"
            mocked_s3_client.put_object(Body="test data".encode(), Bucket=fake_bucket, Key=fake_key)


@pytest.mark.parametrize(
    "s3_folder,expected_number_of_objects",
    [
        (FAKE_S3_FOLDER_ONE, NUMBER_OF_OBJECTS_IN_EACH_FAKE_FOLDER),
        ("", NUMBER_OF_OBJECTS_IN_EACH_FAKE_FOLDER * 2),
    ],
)
def test_list_files_in_s3_folder(
    mocked_s3_client: S3Client,
    fake_bucket: str,
    s3_folder: str,
    expected_number_of_objects: int,
) -> None:
    fake_s3_uri = f"s3://{fake_bucket}/{s3_folder}"
    s3_communicator = S3Communicator(s3_client=mocked_s3_client)
    assert len(s3_communicator.list_files_in_s3_folder(fake_s3_uri)) == expected_number_of_objects


def test_recursive_delete_s3_folder_folder_not_specified(
    mocked_s3_client: S3Client,
    fake_bucket: str,
) -> None:
    fake_s3_uri = f"s3://{fake_bucket}/"
    s3_communicator = S3Communicator(s3_client=mocked_s3_client)
    with pytest.raises(ValueError):
        s3_communicator.recursive_delete_s3_folder(folder_s3_uri=fake_s3_uri)


def test_recursive_delete_s3_folder(
    mocked_s3_client: S3Client,
    fake_bucket: str,
) -> None:
    fake_s3_uri = f"s3://{fake_bucket}/{FAKE_S3_FOLDER_ONE}"
    s3_communicator = S3Communicator(s3_client=mocked_s3_client)
    s3_communicator.recursive_delete_s3_folder(folder_s3_uri=fake_s3_uri)

    assert not s3_communicator.list_files_in_s3_folder(fake_s3_uri)
    assert (
        len(s3_communicator.list_files_in_s3_folder(f"s3://{fake_bucket}/{FAKE_S3_FOLDER_TWO}"))
        == NUMBER_OF_OBJECTS_IN_EACH_FAKE_FOLDER
    )
    assert len(s3_communicator.list_files_in_s3_folder(f"s3://{fake_bucket}/")) == NUMBER_OF_OBJECTS_IN_EACH_FAKE_FOLDER
