from unittest.mock import MagicMock, patch

from src.jobs.cars_silver import run_silver_job


@patch("src.jobs.cars_silver.save_silver_cars")
@patch("src.jobs.cars_silver.transform_cars_spark")
@patch("src.jobs.cars_silver.read_bronze_cars")
@patch("src.jobs.cars_silver.create_spark_session")
def test_run_silver_job(
    mock_create_spark_session,
    mock_read_bronze_cars,
    mock_transform_cars_spark,
    mock_save_silver_cars,
):
    spark = MagicMock()

    bronze_df = MagicMock()
    silver_df = MagicMock()

    mock_create_spark_session.return_value = spark
    mock_read_bronze_cars.return_value = bronze_df
    mock_transform_cars_spark.return_value = silver_df
    mock_save_silver_cars.return_value = "/output"

    result = run_silver_job(
        input_path="/input",
        output_path="/output",
    )

    assert result == "/output"

    mock_create_spark_session.assert_called_once_with()

    mock_read_bronze_cars.assert_called_once_with(
        spark,
        "/input",
    )

    mock_transform_cars_spark.assert_called_once_with(
        bronze_df
    )

    mock_save_silver_cars.assert_called_once_with(
        silver_df,
        "/output",
    )

    spark.stop.assert_called_once_with()