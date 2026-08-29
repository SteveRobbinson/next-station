import json

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
