import logging

from next_station.core.config.settings import settings
from next_station.infrastructure.runner import runner
from next_station.infrastructure.s3 import S3Manager

logger = logging.getLogger(__name__)


def ingest_railway_stations_to_s3():
    logger.info("Starting Railway Stations job")

    try:
        s3 = S3Manager(settings.aws.s3_bucket_name)

        logger.info("Fetching and uploading railway_stations to S3")
        railway_stations = runner(
            api_url=str(settings.api.base_railway_stations_url),
            method="post",
            payload=settings.api.payload_for_railway_stations,
            headers=settings.api.headers,
            stream=True,
        )

        s3.upload_data_to_s3(
            file_name=settings.aws.s3_railway_stations_file_name,
            object_to_upload=railway_stations.raw,
        )
        logger.info("Successfully updated railway stations in S3.")

    except Exception:
        logger.exception("Job failed due to an error")
        raise


if __name__ == "__main__":
    ingest_railway_stations_to_s3()
