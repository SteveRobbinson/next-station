import logging

from next_station.core.config.settings import settings
from next_station.infrastructure.runner import execute_request
from next_station.infrastructure.s3 import S3Manager
from next_station.providers import population_grid
from next_station.schemas.http import APIEndpointConfig

logger = logging.getLogger(__name__)


def ingest_population_grid_to_s3() -> None:
    logger.info("Starting Population Grid job")

    try:
        s3 = S3Manager(settings.aws.s3_bucket_name)
        api_grid_url = population_grid.get_file_url(
            str(settings.api.base_population_grid_url)
        )

        logger.info(f"Checking for updates at: {api_grid_url}")
        s3_grid_metadata = s3.get_object_metadata(
            file_path=settings.aws.s3_population_grid_file_name
        )
        api_grid_metadata = population_grid.fetch_metadata(api_grid_url)

        if s3_grid_metadata != api_grid_metadata:
            logger.info(
                "Change detected. Fetching and processing new population grid..."
            )

            api_endpoint = APIEndpointConfig(method="GET", url=api_grid_url)
            population_grid_data = execute_request(api_endpoint)

            s3.upload_data_to_s3(
                file_name=settings.aws.s3_population_grid_file_name,
                object_to_upload=population_grid_data.raw,
                metadata=api_grid_metadata
            )

            logger.info("Successfully updated population grid in S3.")

        else:
            logger.info("Metadata is identical. Skipping update to save resources.")

    except Exception:
        logger.exception("An UNEXPECTED error occurred, job failed")
        raise


if __name__ == "__main__":
    ingest_population_grid_to_s3()
