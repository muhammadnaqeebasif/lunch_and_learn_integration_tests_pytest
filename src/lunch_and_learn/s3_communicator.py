from typing import List, Optional, Sequence

import boto3
from mypy_boto3_s3 import S3Client
from mypy_boto3_s3.type_defs import ObjectIdentifierTypeDef

from lunch_and_learn.s3_utils import SLASH_LITERAL, split_s3_uri


class S3Communicator:
    def __init__(self: "S3Communicator", s3_client: Optional[S3Client] = None) -> None:
        self.s3_client = s3_client if s3_client else boto3.client("s3")

    def list_files_in_s3_folder(
        self: "S3Communicator",
        folder_s3_uri: str,
        page_size: int = 1000,
    ) -> List[str]:
        bucket, prefix = split_s3_uri(folder_s3_uri)
        if prefix:
            prefix = prefix if prefix.endswith(SLASH_LITERAL) else f"{prefix}/"

        paginator = self.s3_client.get_paginator("list_objects_v2")
        keys_to_return: List[str] = []
        for page in paginator.paginate(  # noqa: WPS352
            Bucket=bucket,
            Prefix=prefix,
            PaginationConfig={"PageSize": page_size},
        ):
            for page_content in page.get("Contents", []):
                keys_to_return.append(page_content["Key"])

        return keys_to_return

    def recursive_delete_s3_folder(  # noqa: WPS210
        self: "S3Communicator",
        folder_s3_uri: str,
        page_size: int = 1000,
    ) -> bool:
        bucket, prefix = split_s3_uri(folder_s3_uri)
        if not prefix:
            raise ValueError("Speficy a prefix to continue")

        delete_us: List[ObjectIdentifierTypeDef] = [
            {"Key": key_to_delete}
            for key_to_delete in self.list_files_in_s3_folder(folder_s3_uri=folder_s3_uri, page_size=page_size)
        ]
        errors = []
        for item_num in range(0, len(delete_us), page_size):
            batch: Sequence[ObjectIdentifierTypeDef] = delete_us[item_num : item_num + page_size]
            response = self.s3_client.delete_objects(
                Bucket=bucket,
                Delete={"Objects": batch, "Quiet": False},
            )
            errors.extend(response.get("Errors", []))

        return not errors
