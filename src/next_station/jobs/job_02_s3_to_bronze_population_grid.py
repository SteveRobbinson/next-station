import logging

from next_station.core.config.settings import settings
from next_station.infrastructure.spark import SparkManager
from next_station.transformations.spark_helpers import extract_population_points

logger = logging.getLogger(__name__)


def load_population_grid_to_databricks():
    logger.info("Initiating population grid load to Databricks Bronze layer")

    try:
        spark = SparkManager()

        logger.info(f"Ingesting raw data from {settings.aws.population_grid_uri}")
        raw_df = spark.read_from_s3(
            aws_s3_path=settings.aws.population_grid_uri, data_format="binaryFile"
        )

        logger.info("Extracting population points from raw dataset")
        df_exploded = extract_population_points(raw_df)

        logger.info(
            f"Persisting exploded dataset to table: {settings.databricks.population_grid_bronze_fqn}"
        )
        spark.save_df_in_databricks(
            df_exploded, settings.databricks.population_grid_bronze_fqn
        )

        logger.info("Successfully completed population grid load to Databricks")

    except Exception:
        logger.error(
            "An error occurred while processing and uploading data to databricks"
        )
        raise


if __name__ == "__main__":
    load_population_grid_to_databricks()
