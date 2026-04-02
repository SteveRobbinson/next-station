from databricks.connect import DatabricksSession
from pyspark.sql import SparkSession

def get_spark_session(user: str) -> SparkSession:

    spark = DatabricksSession.builder.profile(user).getOrCreate()

    return spark
