from collections import Counter


def calculate_car_metrics(
    cars: list[dict],
) -> dict:
    """
    Calcula métricas agregadas
    a partir dos veículos da camada Silver.
    """

    total_cars = len(cars)

    brands = [
        car.get("brand")
        for car in cars
        if car.get("brand")
    ]

    fuel_types = [
        car.get("fuel")
        for car in cars
        if car.get("fuel")
    ]

    transmissions = [
        car.get("transmission")
        for car in cars
        if car.get("transmission")
    ]

    conditions = [
        car.get("condition")
        for car in cars
        if car.get("condition")
    ]

    mileages = [
        car.get("mileage")
        for car in cars
        if car.get("mileage") is not None
    ]

    prices = [
        car.get("price_effective")
        for car in cars
        if car.get("price_effective") is not None
    ]

    price_differences = [
        car.get("price_difference_fipe_percent")
        for car in cars
        if car.get(
            "price_difference_fipe_percent"
        ) is not None
    ]

    views = [
        car.get("views")
        for car in cars
        if car.get("views") is not None
    ]

    metrics = {

        # =====================================
        # VOLUME
        # =====================================

        "total_cars": total_cars,

        # =====================================
        # DISTRIBUIÇÕES
        # =====================================

        "cars_by_brand": dict(
            Counter(brands)
        ),

        "cars_by_fuel": dict(
            Counter(fuel_types)
        ),

        "cars_by_transmission": dict(
            Counter(transmissions)
        ),

        "cars_by_condition": dict(
            Counter(conditions)
        ),

        # =====================================
        # MÉDIAS
        # =====================================

        "average_mileage": (
            sum(
                float(mileage)
                for mileage in mileages
            )
            / len(mileages)
            if mileages
            else None
        ),

        "average_price": (
            sum(
                float(price)
                for price in prices
            )
            / len(prices)
            if prices
            else None
        ),

        "average_price_difference_fipe_percent": (
            sum(
                float(difference)
                for difference in price_differences
            )
            / len(price_differences)
            if price_differences
            else None
        ),

        "average_views": (
            sum(
                float(view)
                for view in views
            )
            / len(views)
            if views
            else None
        ),
    }

    return metrics