import pytest
import boto3
from moto import mock_aws


@pytest.fixture
def mock_s3_env():
    with mock_aws():
        s3 = boto3.client('s3', 'us-east-1')
        bucket_name = 'test_bucket_name'
        s3.create_bucket(Bucket=bucket_name)
        yield bucket_name
