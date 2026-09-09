from unittest.mock import MagicMock, patch

import pytest

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
        run_id="run_test_001",
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


@patch("src.jobs.cars_silver.logger")
@patch("src.jobs.cars_silver.save_silver_cars")
@patch("src.jobs.cars_silver.transform_cars_spark")
@patch("src.jobs.cars_silver.read_bronze_cars")
@patch("src.jobs.cars_silver.create_spark_session")
def test_run_silver_job_logs_run_id(
    mock_create_spark_session,
    mock_read_bronze_cars,
    mock_transform_cars_spark,
    mock_save_silver_cars,
    mock_logger,
):
    spark = MagicMock()

    mock_create_spark_session.return_value = spark
    mock_read_bronze_cars.return_value = MagicMock()
    mock_transform_cars_spark.return_value = MagicMock()
    mock_save_silver_cars.return_value = "/output"

    run_silver_job(
        input_path="/input",
        output_path="/output",
        run_id="run_test_002",
    )

    log_messages = [
        call.args[0]
        for call in mock_logger.info.call_args_list
    ]

    assert any(
        "run_id=%s" in message
        for message in log_messages
    )

    assert any(
        "Job Bronze -> Silver iniciado" in message
        for message in log_messages
    )

    assert any(
        "Job Bronze -> Silver concluído com sucesso" in message
        for message in log_messages
    )


@patch("src.jobs.cars_silver.logger")
@patch("src.jobs.cars_silver.save_silver_cars")
@patch("src.jobs.cars_silver.transform_cars_spark")
@patch("src.jobs.cars_silver.read_bronze_cars")
@patch("src.jobs.cars_silver.create_spark_session")
def test_run_silver_job_logs_and_raises_on_error(
    mock_create_spark_session,
    mock_read_bronze_cars,
    mock_transform_cars_spark,
    mock_save_silver_cars,
    mock_logger,
):
    spark = MagicMock()

    mock_create_spark_session.return_value = spark

    error = RuntimeError("Transformation failed")

    mock_read_bronze_cars.return_value = MagicMock()
    mock_transform_cars_spark.side_effect = error

    with pytest.raises(RuntimeError, match="Transformation failed"):
        run_silver_job(
            input_path="/input",
            output_path="/output",
            run_id="run_test_003",
        )

    mock_logger.exception.assert_called_once()

    exception_message = (
        mock_logger.exception.call_args.args[0]
    )

    assert "Job Bronze -> Silver falhou" in exception_message

    assert "run_id=%s" in exception_message

    spark.stop.assert_called_once_with()