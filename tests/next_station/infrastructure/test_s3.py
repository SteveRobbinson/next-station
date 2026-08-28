import pytest
import boto3
from moto import mock_aws

from next_station.infrastructure.s3 import S3Manager


@pytest.fixture
def mock_s3_env():
    with mock_aws():
        s3 = boto3.client('s3', 'us-east-1')
        bucket_name = 'test_bucket_name'
        s3.create_bucket(Bucket=bucket_name)
        yield bucket_name


def test_s3manager_init_success(mock_s3_env):

    manager = S3Manager(aws_s3_bucket_name=mock_s3_env)

    assert manager.aws_s3_bucket_name == mock_s3_env
    assert manager.s3 is not None
