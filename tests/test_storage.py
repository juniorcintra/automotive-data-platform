import json

from src.storage import cars as storage


def test_save_raw_cars(tmp_path, monkeypatch):
    monkeypatch.setattr(
        storage,
        "DATA_DIR",
        tmp_path,
    )

    data = {
        "data": [
            {
                "id": "1",
                "marca": "Toyota",
                "modelo": "Corolla",
            }
        ]
    }

    file_path = storage.save_raw_cars(data)

    assert file_path.exists()

    assert "bronze" in str(file_path)
    assert file_path.name == "cars.json"

    with open(
        file_path,
        "r",
        encoding="utf-8",
    ) as file:
        saved_data = json.load(file)

    assert saved_data == data


def test_save_processed_cars(tmp_path, monkeypatch):
    monkeypatch.setattr(
        storage,
        "DATA_DIR",
        tmp_path,
    )

    data = [
        {
            "car_id": "1",
            "brand": "Toyota",
            "model": "Corolla",
        }
    ]

    file_path = storage.save_processed_cars(data)

    assert file_path.exists()

    assert "silver" in str(file_path)
    assert file_path.name == "cars.json"

    with open(
        file_path,
        "r",
        encoding="utf-8",
    ) as file:
        saved_data = json.load(file)

    assert saved_data == data


def test_load_processed_cars(tmp_path):
    data = [
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

    file_path = tmp_path / "cars.json"

    with open(
        file_path,
        "w",
        encoding="utf-8",
    ) as file:
        json.dump(
            data,
            file,
        )

    loaded_data = storage.load_processed_cars(
        file_path,
    )

    assert loaded_data == data


def test_save_gold_metrics(tmp_path, monkeypatch):
    monkeypatch.setattr(
        storage,
        "DATA_DIR",
        tmp_path,
    )

    metrics = {
        "total_cars": 33,
        "average_price": 85000,
        "brands": {
            "Toyota": 10,
            "Honda": 8,
        },
    }

    file_path = storage.save_gold_metrics(
        metrics,
    )

    assert file_path.exists()

    assert "gold" in str(file_path)
    assert file_path.name == "cars_metrics.json"

    with open(
        file_path,
        "r",
        encoding="utf-8",
    ) as file:
        saved_data = json.load(file)

    assert saved_data == metrics