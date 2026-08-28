from src.transformation.cars import (
    transform_car,
    transform_cars,
)


def test_transform_car():
    car = {
        "id": "123",
        "marca": "Toyota",
        "modelo": "Corolla",
        "ano": 2020,
        "cor": "Prata",
        "versao": "XEi",
        "quilometragem": 50000,
        "combustivel": "Flex",
        "cambio": "Automático",
        "carroceria": "Sedan",
        "status": "disponível",
        "condicao": "seminovo",
        "visualizacoes": 100,
        "createdAt": "2026-08-20",
        "updatedAt": "2026-08-21",
        "comparativoPreco": {
            "precoEfetivo": 100000,
            "precoFipe": 105000,
            "precoMercado": 102000,
            "percentualDiferencaFipe": -4.76,
        },
        "seller": {
            "id": "seller-1",
            "nome": "João",
        },
    }

    result = transform_car(car)

    assert result["car_id"] == "123"
    assert result["brand"] == "Toyota"
    assert result["model"] == "Corolla"
    assert result["year"] == 2020
    assert result["price_effective"] == 100000
    assert result["seller_name"] == "João"


def test_transform_car_without_optional_data():
    car = {
        "id": "123",
        "marca": "Toyota",
        "modelo": "Corolla",
    }

    result = transform_car(car)

    assert result["car_id"] == "123"
    assert result["brand"] == "Toyota"
    assert result["model"] == "Corolla"

    assert result["seller_id"] is None
    assert result["price_effective"] is None


def test_transform_cars():
    cars = [
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

    result = transform_cars(cars)

    assert len(result) == 2

    assert result[0]["car_id"] == "1"
    assert result[0]["brand"] == "Toyota"

    assert result[1]["car_id"] == "2"
    assert result[1]["brand"] == "Honda"