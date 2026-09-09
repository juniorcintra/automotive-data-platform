from pathlib import Path
from unittest.mock import patch
import subprocess

import pytest

from src.core.config import BASE_DIR
from src.pipeline.spark import (
    _to_container_path,
    run_silver_spark_job,
)

def test_to_container_path():
    path = Path(
        "data/bronze/cars/run_test/cars.json"
    )

    result = _to_container_path(path)

    assert result == (
        "/app/data/bronze/cars/run_test/cars.json"
    )


@patch("src.pipeline.spark.subprocess.run")
def test_run_silver_spark_job(mock_subprocess_run):
    input_path = Path(
        "data/bronze/cars/run_test/cars.json"
    )

    output_path = Path(
        "data/silver_spark/cars/run_test"
    )

    result = run_silver_spark_job(
        input_path=input_path,
        output_path=output_path,
        run_id="run_test",
    )

    assert result == output_path

    mock_subprocess_run.assert_called_once_with(
        [
            "docker",
            "compose",
            "exec",
            "-T",
            "spark",
            "/opt/spark/bin/spark-submit",
            "src/jobs/cars_silver.py",
            "--input",
            "/app/data/bronze/cars/run_test/cars.json",
            "--output",
            "/app/data/silver_spark/cars/run_test",
            "--run-id",
            "run_test",
        ],
        cwd=BASE_DIR,
        check=True,
    )

@patch("src.pipeline.spark.subprocess.run")
def test_run_silver_spark_job_propagates_error(
    mock_subprocess_run,
):
    input_path = Path(
        "data/bronze/cars/run_test/cars.json"
    )

    output_path = Path(
        "data/silver_spark/cars/run_test"
    )

    error = subprocess.CalledProcessError(
        returncode=1,
        cmd=["docker", "compose"],
    )

    mock_subprocess_run.side_effect = error

    with pytest.raises(
        subprocess.CalledProcessError
    ):
        run_silver_spark_job(
            input_path=input_path,
            output_path=output_path,
            run_id="run_test",
        )