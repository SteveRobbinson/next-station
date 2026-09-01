import logging

from next_station.core.config.settings import settings
from next_station.infrastructure.runner import runner
from next_station.infrastructure.s3 import S3Manager
from next_station.infrastructure.utils import get_api_object_metadata
from next_station.providers.get_file_url import get_file_url

logger = logging.getLogger(__name__)


def ingest_population_grid_to_s3():
    logger.info("Starting Population Grid job")

    try:
        s3 = S3Manager(settings.aws.s3_bucket_name)
        population_grid_file_url = get_file_url(
            str(settings.api.base_population_grid_url)
        )

        logger.info(f"Checking for updates at: {population_grid_file_url}")
        s3_object_metadata = s3.get_object_metadata(
            file_path=settings.aws.s3_population_grid_file_name
        )
        api_object_metadata = get_api_object_metadata(population_grid_file_url)

        if s3_object_metadata != api_object_metadata:
            logger.info(
                "Change detected. Fetching and processing new population grid..."
            )

            population_grid = runner(
                api_url=population_grid_file_url, method="get", stream=True
            )

            s3.upload_data_to_s3(
                file_name=settings.aws.s3_population_grid_file_name,
                object_to_upload=population_grid.raw,
                metadata=api_object_metadata,
            )

            logger.info("Successfully updated population grid in S3.")

        else:
            logger.info("Metadata is identical. Skipping update to save resources.")

    except Exception:
        logger.exception("An UNEXPECTED error occurred, job failed")
        raise


if __name__ == "__main__":
    ingest_population_grid_to_s3()
