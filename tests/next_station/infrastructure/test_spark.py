from next_station.infrastructure.spark import SparkManager


def test_verify_binary_reads(tmp_path):
    file_path = tmp_path / "binary_data"
    file_path.write_bytes(b"test data")

    spark = SparkManager()
    spark_read = spark.read_from_s3(aws_s3_path=str(file_path), data_format='binaryFile').first()['content']
    
    assert spark_read == b"test data"
    

