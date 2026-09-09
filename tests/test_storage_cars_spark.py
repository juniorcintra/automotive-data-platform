from pathlib import Path
from unittest.mock import MagicMock

from src.storage.cars_spark import (
    load_silver_cars,
)


def test_load_silver_cars():
    spark = MagicMock()

    row_1 = MagicMock()
    row_1.asDict.return_value = {
        "car_id": "1",
        "brand": "Toyota",
        "model": "Corolla",
    }

    row_2 = MagicMock()
    row_2.asDict.return_value = {
        "car_id": "2",
        "brand": "Honda",
        "model": "Civic",
    }

    cars_df = MagicMock()
    cars_df.collect.return_value = [
        row_1,
        row_2,
    ]

    spark.read.parquet.return_value = cars_df

    result = load_silver_cars(
        spark=spark,
        input_path=Path(
            "data/silver_spark/cars/run_test"
        ),
    )

    assert result == [
        {
            "car_id": "1",
            "brand": "Toyota",
            "model": "Corolla",
        },
        {
            "car_id": "2",
            "brand": "Honda",
            "model": "Civic",
        },
    ]

    spark.read.parquet.assert_called_once_with(
        "data/silver_spark/cars/run_test"
    )

    cars_df.collect.assert_called_once_with()