import logging

from next_station.infrastructure.spark import SparkManager
from next_station.transformations.spark_helpers import explode_and_flatten
from next_station.core.config.settings import settings

logger = logging.getLogger(__name__)

def load_railway_stations_to_databricks():
    logger.info('Initiating railway stations load to Databricks Bronze layer')

    try:
        spark = SparkManager()

        logger.info(f"Ingesting raw data from {settings.aws.railway_stations_uri}")
        df_raw = spark.read_from_s3(aws_s3_path=settings.aws.railway_stations_uri, data_format='json')

        logger.info("Table transformations")
        df_processed = explode_and_flatten(df=df_raw, explode_by=settings.aws.railway_file_explode_by)

        logger.info("Uploading table to databricks")
        spark.save_df_in_databricks(df=df_processed,
                                    table_name=settings.databricks.railway_stations_bronze_fqn)

        logger.info("Successfully loaded railway stations to Databricks")

    except Exception:
        logger.error("An error occurred while uploading railway stations to databricks")
        raise

if __name__ == '__main__':
    load_railway_stations_to_databricks()
