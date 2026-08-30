import logging

from next_station.infrastructure.spark import SparkManager
from next_station.core.config.settings import settings

logger = logging.getLogger(__name__)

def run_export_job():
    tasks = settings.export_tasks
    logger.info(f"Starting export job for {len(tasks)} tasks")
    
    try:
        spark = SparkManager()

        for task in settings.export_tasks:
            spark.export_table_to_s3(table_name=task.databricks_fqn, aws_bucket_uri=task.aws_target_uri)

        logger.info("All export tasks completed successfully")

    except Exception:
        logger.error("Export job aborted due to an error")
        raise

if __name__ == "__main__":
    run_export_job()
