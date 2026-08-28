from src.quality.cars import (
    validate_car,
    find_duplicate_ids,
)


def test_validate_valid_car():
    car = {
        "id": "123",
        "marca": "Toyota",
        "modelo": "Corolla",
        "ano": 2020,
        "quilometragem": 50000,
        "comparativoPreco": {
            "precoEfetivo": 100000,
        },
    }

    errors = validate_car(car)

    assert errors == []


def test_validate_car_without_id():
    car = {
        "marca": "Toyota",
        "modelo": "Corolla",
        "ano": 2020,
        "quilometragem": 50000,
        "comparativoPreco": {
            "precoEfetivo": 100000,
        },
    }

    errors = validate_car(car)

    assert "ID ausente" in errors


def test_validate_car_without_brand():
    car = {
        "id": "123",
        "modelo": "Corolla",
        "ano": 2020,
        "quilometragem": 50000,
        "comparativoPreco": {
            "precoEfetivo": 100000,
        },
    }

    errors = validate_car(car)

    assert "Marca ausente" in errors


def test_validate_car_with_invalid_year():
    car = {
        "id": "123",
        "marca": "Toyota",
        "modelo": "Corolla",
        "ano": 1800,
        "quilometragem": 50000,
        "comparativoPreco": {
            "precoEfetivo": 100000,
        },
    }

    errors = validate_car(car)

    assert "Ano inválido: 1800" in errors


def test_validate_car_with_invalid_price():
    car = {
        "id": "123",
        "marca": "Toyota",
        "modelo": "Corolla",
        "ano": 2020,
        "quilometragem": 50000,
        "comparativoPreco": {
            "precoEfetivo": 0,
        },
    }

    errors = validate_car(car)

    assert "Preço efetivo inválido: 0" in errors


def test_validate_car_with_negative_mileage():
    car = {
        "id": "123",
        "marca": "Toyota",
        "modelo": "Corolla",
        "ano": 2020,
        "quilometragem": -100,
        "comparativoPreco": {
            "precoEfetivo": 100000,
        },
    }

    errors = validate_car(car)

    assert "Quilometragem inválida: -100" in errors


def test_find_duplicate_ids():
    cars = [
        {"id": "1"},
        {"id": "2"},
        {"id": "1"},
        {"id": "3"},
        {"id": "2"},
    ]

    duplicate_ids = find_duplicate_ids(cars)

    assert "1" in duplicate_ids
    assert "2" in duplicate_ids
    assert len(duplicate_ids) == 2


def test_find_duplicate_ids_without_duplicates():
    cars = [
        {"id": "1"},
        {"id": "2"},
        {"id": "3"},
    ]

    duplicate_ids = find_duplicate_ids(cars)

    assert duplicate_ids == []