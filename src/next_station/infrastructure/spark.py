import logging

from pyspark.sql import SparkSession


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

