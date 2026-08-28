import pytest

from src.analytics.cars import (
    calculate_car_metrics,
)


def test_calculate_car_metrics():
    cars = [
        {
            "brand": "Hyundai",
            "fuel": "Flex",
            "transmission": "Manual",
            "condition": "seminovo",
            "mileage": 10000,
            "price_effective": 50000,
            "price_difference_fipe_percent": 5,
            "views": 10,
        },
        {
            "brand": "Toyota",
            "fuel": "Flex",
            "transmission": "Automatico",
            "condition": "usado",
            "mileage": 20000,
            "price_effective": 60000,
            "price_difference_fipe_percent": 10,
            "views": 20,
        },
        {
            "brand": "Hyundai",
            "fuel": "Gasolina",
            "transmission": "Automatico",
            "condition": "seminovo",
            "mileage": 30000,
            "price_effective": 70000,
            "price_difference_fipe_percent": 15,
            "views": 30,
        },
    ]

    metrics = calculate_car_metrics(cars)

    assert metrics["total_cars"] == 3

    assert metrics["cars_by_brand"] == {
        "Hyundai": 2,
        "Toyota": 1,
    }

    assert metrics["cars_by_fuel"] == {
        "Flex": 2,
        "Gasolina": 1,
    }

    assert metrics["cars_by_transmission"] == {
        "Manual": 1,
        "Automatico": 2,
    }

    assert metrics["cars_by_condition"] == {
        "seminovo": 2,
        "usado": 1,
    }

    assert metrics["average_mileage"] == 20000.0

    assert metrics["average_price"] == 60000.0

    assert (
        metrics[
            "average_price_difference_fipe_percent"
        ]
        == 10.0
    )

    assert metrics["average_views"] == 20.0


def test_calculate_car_metrics_with_empty_list():
    metrics = calculate_car_metrics([])

    assert metrics["total_cars"] == 0

    assert metrics["cars_by_brand"] == {}

    assert metrics["cars_by_fuel"] == {}

    assert metrics["cars_by_transmission"] == {}

    assert metrics["cars_by_condition"] == {}

    assert metrics["average_mileage"] is None

    assert metrics["average_price"] is None

    assert (
        metrics[
            "average_price_difference_fipe_percent"
        ]
        is None
    )

    assert metrics["average_views"] is None


def test_calculate_car_metrics_ignores_missing_optional_values():
    cars = [
        {
            "brand": "Hyundai",
            "fuel": "Flex",
            "transmission": "Manual",
            "condition": "seminovo",
            "mileage": 10000,
            "price_effective": 50000,
            "price_difference_fipe_percent": 5,
            "views": 10,
        },
        {
            "brand": "Toyota",
            "fuel": None,
            "transmission": None,
            "condition": None,
            "mileage": None,
            "price_effective": None,
            "price_difference_fipe_percent": None,
            "views": None,
        },
    ]

    metrics = calculate_car_metrics(cars)

    assert metrics["total_cars"] == 2

    assert metrics["cars_by_brand"] == {
        "Hyundai": 1,
        "Toyota": 1,
    }

    assert metrics["cars_by_fuel"] == {
        "Flex": 1,
    }

    assert metrics["cars_by_transmission"] == {
        "Manual": 1,
    }

    assert metrics["cars_by_condition"] == {
        "seminovo": 1,
    }

    assert metrics["average_mileage"] == 10000.0

    assert metrics["average_price"] == 50000.0

    assert (
        metrics[
            "average_price_difference_fipe_percent"
        ]
        == 5.0
    )

    assert metrics["average_views"] == 10.0


def test_calculate_car_metrics_with_numeric_strings():
    cars = [
        {
            "brand": "Honda",
            "fuel": "Flex",
            "transmission": "Automatico",
            "condition": "seminovo",
            "mileage": "10000",
            "price_effective": "50000",
            "price_difference_fipe_percent": "5.5",
            "views": "20",
        },
        {
            "brand": "Honda",
            "fuel": "Flex",
            "transmission": "Automatico",
            "condition": "seminovo",
            "mileage": "20000",
            "price_effective": "70000",
            "price_difference_fipe_percent": "10.5",
            "views": "40",
        },
    ]

    metrics = calculate_car_metrics(cars)

    assert metrics["total_cars"] == 2

    assert metrics["average_mileage"] == 15000.0

    assert metrics["average_price"] == 60000.0

    assert (
        metrics[
            "average_price_difference_fipe_percent"
        ]
        == 8.0
    )

    assert metrics["average_views"] == 30.0