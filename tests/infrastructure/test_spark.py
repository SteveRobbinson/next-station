from unittest.mock import MagicMock

from next_station.infrastructure.spark import SparkManager


def test_verify_binary_reads() -> None:
    file_path = "test/path/binary_data"
    mock_session = MagicMock()
    mock_df = MagicMock()
    mock_session.read.format.return_value.load.return_value = mock_df
    spark = SparkManager(spark_session=mock_session, sedona_context=mock_session)

    result = spark.read_from_s3(aws_s3_path=file_path, data_format="binaryFile")

    mock_session.read.format.assert_called_once_with("binaryFile")
    mock_session.read.format.return_value.load.assert_called_once_with(file_path)
    assert result == mock_df


def test_verify_json_reads() -> None:
    file_path = "test_data.json"
    mock_session = MagicMock()
    mock_df = MagicMock()
    mock_session.read.format.return_value.option.return_value.load.return_value = (
        mock_df
    )
    spark = SparkManager(spark_session=mock_session, sedona_context=mock_session)

    result = spark.read_from_s3(aws_s3_path=str(file_path), data_format="json")

    mock_session.read.format.assert_called_once_with("json")
    mock_session.read.format.return_value.option.assert_called_once_with(
        "multiLine", "true"
    )
    mock_session.read.format.return_value.option.return_value.load.assert_called_once_with(
        file_path
    )
    assert result == mock_df


def test_save_df_in_databricks() -> None:
    mock_df = MagicMock()
    table_name = "silver.test_data"

    SparkManager.save_df_in_databricks(
        df=mock_df,
        table_name=table_name,
        save_format="delta",
        save_mode="overwrite",
        merge_schema=True,
    )

    mock_df.write.format.assert_called_once_with("delta")
    mock_df.write.format().mode.assert_called_once_with("overwrite")
    mock_df.write.format().mode().option.assert_called_once_with("mergeSchema", True)
    mock_df.write.format().mode().option().saveAsTable.assert_called_once_with(
        table_name
    )
