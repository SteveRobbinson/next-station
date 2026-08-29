from next_station.core.exceptions.base import BaseAppError

class SparkRelatedError(BaseAppError):
    default_message = "A Spark-related error occurred."

class SparkInitError(SparkRelatedError):
    default_message = "Failed to initialize Spark session."

class SparkReadError(SparkRelatedError):
    default_message = "Failed to read data using Spark."

class SparkSaveError(SparkRelatedError):
    default_message = "Failed to save data using Spark."
