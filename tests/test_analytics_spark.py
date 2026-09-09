from src.analytics.cars_spark import (
    calculate_car_metrics_spark,
)
from src.transformation.cars_spark import (
    create_spark_session,
)


def test_calculate_car_metrics_spark():
    spark = create_spark_session()

    try:
        cars_df = spark.createDataFrame(
            [
                (
                    "1",
                    "Toyota",
                    "Corolla",
                    45000.0,
                    "Flex",
                    "Automático",
                    "Usado",
                    120000.0,
                    -3.0,
                    150,
                ),
                (
                    "2",
                    "Toyota",
                    "Yaris",
                    30000.0,
                    "Flex",
                    "Automático",
                    "Usado",
                    100000.0,
                    -4.0,
                    100,
                ),
                (
                    "3",
                    "Honda",
                    "Civic",
                    60000.0,
                    "Flex",
                    "Manual",
                    "Usado",
                    140000.0,
                    -3.5,
                    200,
                ),
            ],
            [
                "car_id",
                "brand",
                "model",
                "mileage",
                "fuel",
                "transmission",
                "condition",
                "price_effective",
                "price_difference_fipe_percent",
                "views",
            ],
        )

        metrics = calculate_car_metrics_spark(
            cars_df
        )

        assert metrics == {
            "total_cars": 3,
            "cars_by_brand": {
                "Toyota": 2,
                "Honda": 1,
            },
            "cars_by_fuel": {
                "Flex": 3,
            },
            "cars_by_transmission": {
                "Automático": 2,
                "Manual": 1,
            },
            "cars_by_condition": {
                "Usado": 3,
            },
            "average_mileage": 45000.0,
            "average_price": 120000.0,
            "average_price_difference_fipe_percent": (
                -3.5
            ),
            "average_views": 150.0,
        }

    finally:
        spark.stop()