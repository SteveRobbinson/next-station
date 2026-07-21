from __future__ import annotations
import logging
from next_station.core.types import SupportsRead
import json
import boto3
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from mypy_boto3_s3 import S3Client
from .runner import runner
from next_station.schemas.worldpop import ApiMetadata, S3Etag
from next_station.core.exceptions.external import AWSServiceError
from next_station.core.config.settings import settings
from botocore.exceptions import ClientError

logger = logging.getLogger(__name__)

def create_s3_client() -> S3Client:

    logger.info("Started creating S3 client")

    try:
        s3 = boto3.client('s3')
        s3.head_bucket(Bucket=settings.aws.s3_bucket_name)
        logger.info("Successfully created S3 client")
        return s3
    
    except Exception as err:
        raise AWSServiceError.from_exception(err) from err


def get_s3_object_metadata(s3client: S3Client,
                           aws_s3_bucket_name: str,
                           metadata_file_path: str,
                           ) -> dict | None:

    logger.info(f"Retrieving metadata from {metadata_file_path}")

    try:
        aws_response = s3client.get_object(
            Bucket = aws_s3_bucket_name,
            Key = metadata_file_path)

        metadata = json.load(aws_response['Body'])
        ### model pydantic, walidacja schematu json, do zrobienia
        logger.info(f"Successfully retrieved metadata from {aws_s3_bucket_name}/{metadata_file_path}")
        return metadata

    
    except ClientError as err:
        if err.response['Error']['Code'] == 'NoSuchKey':
            return None

        raise AWSServiceError.from_exception(err) from err


def compare_metadata(s3_metadata: dict | None,
                     file_url: str
                    ) -> bool:
    
    logger.info(f"Comparing metadata for {file_url}")

    if not s3_metadata:
        logger.warning(f"Comparison aborted: No metadata available for {file_url}")
        return False

    try:
        api_response = runner(file_url, 'head')
        api_etag = ApiMetadata(**api_response.headers).etag
        aws_s3_etag = S3Etag(**s3_metadata).s3_etag

        is_match = aws_s3_etag == api_etag
        logger.info(f"Metadata match for {file_url}: {is_match}")
        return is_match
    

    except Exception as err:
        # Tutaj musze uzyc UnifiedAPIError zamiast AWSServiceError
        raise AWSServiceError.from_exception(err) from err


def upload_data_to_s3(bucket_name: str,
                      file_name: str,
                      object_to_upload: SupportsRead,
                      s3_client: S3Client,
                      metadata: dict | None = None
                      ) -> bool:

    logger.info(f"Starting uploading {file_name} to bucket {bucket_name}")
    extra_args = {'Metadata': metadata} if metadata else {}

    try:
        logger.info(f"Uploading object to S3: {file_name}")
        s3_client.upload_fileobj(Bucket = bucket_name,
                             Fileobj = object_to_upload,
                             Key = file_name,
                             ExtraArgs = extra_args)
        
        if metadata:
            metadata_content = json.dumps(metadata).encode('utf-8')
            metadata_key = f"{file_name}/metadata.json"
            logger.info(f"Uploading metadata file to S3: {metadata_key}")
            s3_client.put_object(
                    Bucket = bucket_name,
                    Key = metadata_key,
                    Body = metadata_content
                    )


        logger.info(f"Successfully finished all upload operations for {file_name}")
        return True

    except Exception as err:
        logger.exception(f"Critical failure during S3 upload of {file_name}")
        raise AWSServiceError.from_exception(err) from err
