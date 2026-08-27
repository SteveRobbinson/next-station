from __future__ import annotations
import logging
import boto3
from next_station.core.exceptions.external import AWSServiceError
from next_station.core.config.settings import settings
from botocore.exceptions import ClientError
import io

logger = logging.getLogger(__name__)

class S3Manager:
    def __init__(self, aws_s3_bucket_name: str) -> None:
        logger.info("Initializing S3 client")

        try:
            s3 = boto3.client('s3')
            s3.head_bucket(Bucket=settings.aws.s3_bucket_name)
            logger.info("Successfully initialized S3 client")

            self.s3 = s3
            self.aws_s3_bucket_name = aws_s3_bucket_name

        except Exception as err:
            raise AWSServiceError.from_exception(err) from err


    def get_s3_object(self,
                      file_path: str
                      ) -> bytes | None:

        logger.info(f"Retrieving object from {file_path}")

        try:
            aws_response = self.s3.get_object(
                Bucket = self.aws_s3_bucket_name,
                Key = file_path)

            logger.info(f"Successfully retrieved object from {self.aws_s3_bucket_name}/{file_path}")
            return aws_response['Body'].read()
        
        except ClientError as err:
            if err.response['Error']['Code'] == 'NoSuchKey':
                return None

            raise AWSServiceError.from_exception(err) from err

    def upload_data_to_s3(self,
                          file_name: str,
                          object_to_upload: io.BytesIO,
                          metadata: dict | None = None
                          ) -> bool:

        logger.info(f"Starting uploading {file_name} to bucket {self.aws_s3_bucket_name}")
        extra_args = {'Metadata': metadata} if metadata else {}

        try:
            logger.info(f"Uploading object to S3: {file_name}")
            self.s3.upload_fileobj(Bucket = self.aws_s3_bucket_name,
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
