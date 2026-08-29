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

