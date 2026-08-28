from pathlib import Path
from unittest.mock import patch

from src.pipeline.cars import main


def test_pipeline_execution():
    raw_cars = [
        {
            "id": "1",
            "marca": "Toyota",
            "modelo": "Corolla",
        },
        {
            "id": "2",
            "marca": "Honda",
            "modelo": "Civic",
        },
    ]

    valid_cars = raw_cars

    invalid_cars = []

    transformed_cars = [
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

    metrics = {
        "total_cars": 2,
    }

    with (
        patch(
            "src.pipeline.cars.get_all_cars",
            return_value=raw_cars,
        ) as mock_get_all_cars,

        patch(
            "src.pipeline.cars.save_raw_cars",
            return_value=Path(
                "data/bronze/cars.json"
            ),
        ) as mock_save_raw_cars,

        patch(
            "src.pipeline.cars.validate_cars",
            return_value=(
                valid_cars,
                invalid_cars,
            ),
        ) as mock_validate_cars,

        patch(
            "src.pipeline.cars.transform_cars",
            return_value=transformed_cars,
        ) as mock_transform_cars,

        patch(
            "src.pipeline.cars.save_processed_cars",
            return_value=Path(
                "data/silver/cars.json"
            ),
        ) as mock_save_processed_cars,

        patch(
            "src.pipeline.cars.load_processed_cars",
            return_value=transformed_cars,
        ) as mock_load_processed_cars,

        patch(
            "src.pipeline.cars.calculate_car_metrics",
            return_value=metrics,
        ) as mock_calculate_metrics,

        patch(
            "src.pipeline.cars.save_gold_metrics",
            return_value=Path(
                "data/gold/cars_metrics.json"
            ),
        ) as mock_save_gold_metrics,
    ):

        main()

    # ========================================
    # INGESTION
    # ========================================

    mock_get_all_cars.assert_called_once_with()

    # ========================================
    # BRONZE
    # ========================================

    mock_save_raw_cars.assert_called_once_with(
        {
            "data": raw_cars,
        }
    )

    # ========================================
    # DATA QUALITY
    # ========================================

    mock_validate_cars.assert_called_once_with(
        raw_cars
    )

    # ========================================
    # TRANSFORMATION
    # ========================================

    mock_transform_cars.assert_called_once_with(
        valid_cars
    )

    # ========================================
    # SILVER
    # ========================================

    mock_save_processed_cars.assert_called_once_with(
        transformed_cars
    )

    mock_load_processed_cars.assert_called_once_with(
        Path("data/silver/cars.json")
    )

    # ========================================
    # GOLD / ANALYTICS
    # ========================================

    mock_calculate_metrics.assert_called_once_with(
        transformed_cars
    )

    mock_save_gold_metrics.assert_called_once_with(
        metrics
    )