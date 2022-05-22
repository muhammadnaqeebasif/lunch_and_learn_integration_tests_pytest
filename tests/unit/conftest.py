from typing import Generator

import boto3
import pytest
from moto import mock_s3
from mypy_boto3_s3 import S3Client

AWS_REGION_NAME = "us-east-1"


@pytest.fixture(name="fake_bucket")
def fake_bucket_fixture() -> str:
    return "fake_bucket"


@pytest.fixture(name="mocked_s3_client")
def fixture_s3_client(fake_bucket: str) -> Generator[S3Client, None, None]:
    with mock_s3():
        s3_client = boto3.client("s3", region_name=AWS_REGION_NAME)
        s3_client.create_bucket(Bucket=fake_bucket)
        yield s3_client
