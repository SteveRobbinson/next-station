import logging
from typing import Literal

from pyspark.sql import SparkSession, DataFrame


logger = logging.getLogger(__name__)

class SparkManager:
    def __init__(self) -> None:
        logger.info("Initializing spark session")

        try:
            self.spark = SparkSession.builder.getOrCreate()
            self.spark.range(1).count()

            logger.info("Successfully intialized spark session")

        except Exception as err:
            raise RuntimeError() from err


    def read_from_s3(self,
                     aws_s3_path: str,
                     data_format: Literal['json', 'binaryFile']
                     ) -> DataFrame:

        logger.info(f"Started fetching data from {aws_s3_path}")

        try:
            if data_format == 'json':
                df = self.spark.read.format(data_format).option('multiLine', 'true').load(aws_s3_path)

            elif data_format == 'binaryFile':
                df = self.spark.read.format(data_format).load(aws_s3_path)

            logger.info(f"Successfully loaded data from {aws_s3_path} to spark")
            return df

        except Exception as err:
            raise RuntimeError() from err


    @staticmethod
    def save_df_in_databricks(df: DataFrame,
                              table_name: str,
                              save_format: str = 'delta',
                              save_mode: str = 'append',
                              merge_schema: bool = False) -> None:

        logger.info(f"Starting write to table: {table_name} (format: {save_format}, mode: {save_mode})")
        
        try:
            df.write.format(save_format).mode(save_mode).option('mergeSchema', merge_schema).saveAsTable(table_name)
            logger.info(f"Table {table_name} saved successfully")

        except Exception as err:
            logger.exception(f"Error occurred while saving table {table_name} to databricks")
            raise RuntimeError() from err
