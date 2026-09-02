import logging
from typing import Literal

from pyspark.sql import DataFrame, SparkSession
from sedona.spark.SedonaContext import SedonaContext

from next_station.core.exceptions.spark import (
    SparkInitError,
    SparkReadError,
    SparkSaveError,
)

logger = logging.getLogger(__name__)


class SparkManager:
    def __init__(self) -> None:
        logger.info("Initializing spark session")

        try:
            self.spark = SparkSession.builder.getOrCreate()
            self.spark = SedonaContext.create(self.spark)
            self.spark.range(1).count()

            logger.info("Successfully intialized spark session")

        except Exception as err:
            logger.exception("Error occurred while initializing spark session")
            raise SparkInitError() from err

    def read_from_s3(
        self, aws_s3_path: str, data_format: Literal["json", "binaryFile"]
    ) -> DataFrame:

        logger.info(f"Started fetching data from {aws_s3_path}")

        try:
            if data_format == "json":
                df = (
                    self.spark.read.format(data_format)
                    .option("multiLine", "true")
                    .load(aws_s3_path)
                )

            elif data_format == "binaryFile":
                df = self.spark.read.format(data_format).load(aws_s3_path)

            logger.info(f"Successfully loaded data from {aws_s3_path} to spark")
            return df

        except Exception as err:
            logger.exception("Error occurred while reading from S3")
            raise SparkReadError() from err

    @staticmethod
    def save_df_in_databricks(
        df: DataFrame,
        table_name: str,
        save_format: str = "delta",
        save_mode: str = "append",
        merge_schema: bool = False,
    ) -> None:

        logger.info(
            f"Starting write to table: {table_name} (format: {save_format}, mode: {save_mode})"
        )

        try:
            df.write.format(save_format).mode(save_mode).option(
                "mergeSchema", merge_schema
            ).saveAsTable(table_name)
            logger.info(f"Table {table_name} saved successfully")

        except Exception as err:
            logger.exception(
                f"Error occurred while saving table {table_name} to databricks"
            )
            raise SparkSaveError() from err

    def export_table_to_s3(
        self,
        table_name: str,
        aws_bucket_uri: str,
        write_mode: str = "overwrite",
        data_format: str = "parquet",
    ) -> None:

        logger.info(
            f"Consolidating table {table_name} into a single parquet file at {aws_bucket_uri}"
        )

        try:
            df = self.spark.table(table_name)

            (df.write.mode(write_mode).format(data_format).save(aws_bucket_uri))

            logger.info(f"Successfully consolidated {table_name} into {aws_bucket_uri}")

        except Exception as err:
            logger.exception("Error occurred while exporting table to s3")
            raise SparkSaveError() from err
