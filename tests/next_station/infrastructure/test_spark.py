import json
from unittest.mock import MagicMock

from next_station.infrastructure.spark import SparkManager


def test_verify_binary_reads(tmp_path):
    file_path = tmp_path / "binary_data"
    file_path.write_bytes(b"test data")

    spark = SparkManager()
    spark_read = spark.read_from_s3(aws_s3_path=str(file_path), data_format='binaryFile').first()['content']
    
    assert spark_read == b"test data"
    

def test_verify_json_reads(tmp_path):
    test_data = {"id": 5, "status": "active", "description": "test data"}

    file_path = tmp_path / "test_data.json"
    file_path.write_text(json.dumps(test_data, indent=4))
    
    spark = SparkManager()
    spark_read = spark.read_from_s3(aws_s3_path=str(file_path), data_format='json').first().asDict()
    
    assert spark_read == test_data


def test_save_df_in_databricks():
    mock_df = MagicMock()
    table_name = "silver.test_data"
    
    SparkManager.save_df_in_databricks(
        df=mock_df,
        table_name=table_name,
        save_format="delta",
        save_mode="overwrite",
        merge_schema=True
    )

    mock_df.write.format.assert_called_once_with("delta")
    mock_df.write.format().mode.assert_called_once_with("overwrite")
    mock_df.write.format().mode().option.assert_called_once_with("mergeSchema", True)
    mock_df.write.format().mode().option().saveAsTable.assert_called_once_with(table_name)
