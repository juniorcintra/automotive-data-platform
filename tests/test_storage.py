from pathlib import Path

from src.storage.cars import (
    load_processed_cars,
    save_gold_metrics,
    save_processed_cars,
    save_raw_cars,
)


def test_save_raw_cars(
    tmp_path,
    monkeypatch,
):
    monkeypatch.setattr(
        "src.storage.cars.DATA_DIR",
        Path(tmp_path),
    )

    data = {
        "data": [
            {
                "id": "1",
                "marca": "Toyota",
            }
        ]
    }

    run_id = "test_run"

    file_path = save_raw_cars(
        data,
        run_id,
    )

    assert file_path.exists()

    assert file_path.suffix == ".json"


def test_save_processed_cars(
    tmp_path,
    monkeypatch,
):
    monkeypatch.setattr(
        "src.storage.cars.DATA_DIR",
        Path(tmp_path),
    )

    cars = [
        {
            "car_id": "1",
            "brand": "Toyota",
            "model": "Corolla",
            "year": 2024,
        },
        {
            "car_id": "2",
            "brand": "Honda",
            "model": "Civic",
            "year": 2023,
        },
    ]

    run_id = "test_run"

    file_path = save_processed_cars(
        cars,
        run_id,
    )

    assert file_path.exists()

    assert file_path.suffix == ".parquet"


def test_load_processed_cars(
    tmp_path,
    monkeypatch,
):
    monkeypatch.setattr(
        "src.storage.cars.DATA_DIR",
        Path(tmp_path),
    )

    cars = [
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

    run_id = "test_run"

    file_path = save_processed_cars(
        cars,
        run_id,
    )

    loaded_cars = load_processed_cars(
        file_path
    )

    assert len(loaded_cars) == 2

    assert loaded_cars[0]["car_id"] == "1"

    assert loaded_cars[0]["brand"] == "Toyota"

    assert loaded_cars[1]["car_id"] == "2"

    assert loaded_cars[1]["brand"] == "Honda"


def test_save_gold_metrics(
    tmp_path,
    monkeypatch,
):
    monkeypatch.setattr(
        "src.storage.cars.DATA_DIR",
        Path(tmp_path),
    )

    metrics = {
        "total_cars": 2,
        "average_price": 50000.0,
    }

    run_id = "test_run"

    file_path = save_gold_metrics(
        metrics,
        run_id,
    )

    assert file_path.exists()

    assert file_path.suffix == ".json"