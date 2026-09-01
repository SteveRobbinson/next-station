import io

import boto3
import pytest
from moto import mock_aws

from next_station.infrastructure.s3 import S3Manager


@pytest.fixture
def mock_s3_env():
    with mock_aws():
        s3 = boto3.client("s3", "us-east-1")
        bucket_name = "test_bucket_name"
        s3.create_bucket(Bucket=bucket_name)
        yield bucket_name


def test_s3manager_init_success(mock_s3_env):

    manager = S3Manager(aws_s3_bucket_name=mock_s3_env)

    assert manager.aws_s3_bucket_name == mock_s3_env
    assert manager.s3 is not None


def test_s3manager_get_object_returns_bytes_when_file_exists(mock_s3_env):
    boto3.client("s3").put_object(
        Bucket=mock_s3_env, Body=b"test data", Key="valid/file/path"
    )
    manager = S3Manager(mock_s3_env)

    result = manager.get_s3_object("valid/file/path")

    assert result == b"test data"


def test_s3manager_get_object_returns_none_when_file_is_missing(mock_s3_env):
    manager = S3Manager(mock_s3_env)

    result = manager.get_s3_object("invalid/file/path")

    assert result is None


def test_s3manager_upload_data_to_s3(mock_s3_env):
    manager = S3Manager(mock_s3_env)
    is_uploaded = manager.upload_data_to_s3(
        file_name="test-file-name", object_to_upload=io.BytesIO(b"test data")
    )

    result = boto3.client("s3").get_object(Bucket=mock_s3_env, Key="test-file-name")

    assert is_uploaded is True
    assert result["Body"].read() == b"test data"
