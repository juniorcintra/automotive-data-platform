from pyspark.sql import DataFrame
from pyspark.sql import functions as F


def calculate_car_metrics_spark(
    cars_df: DataFrame,
) -> dict:
    """
    Calcula métricas agregadas dos veículos utilizando Spark.
    """

    total_cars = (
        cars_df
        .agg(F.count("*").alias("total_cars"))
        .collect()[0]["total_cars"]
    )

    cars_by_brand = (
        cars_df
        .groupBy("brand")
        .count()
        .orderBy(F.desc("count"))
        .collect()
    )

    cars_by_fuel = (
        cars_df
        .groupBy("fuel")
        .count()
        .orderBy(F.desc("count"))
        .collect()
    )

    cars_by_transmission = (
        cars_df
        .groupBy("transmission")
        .count()
        .orderBy(F.desc("count"))
        .collect()
    )

    cars_by_condition = (
        cars_df
        .groupBy("condition")
        .count()
        .orderBy(F.desc("count"))
        .collect()
    )

    averages = (
        cars_df
        .agg(
            F.avg("mileage").alias(
                "average_mileage"
            ),
            F.avg("price_effective").alias(
                "average_price"
            ),
            F.avg(
                "price_difference_fipe_percent"
            ).alias(
                "average_price_difference_fipe_percent"
            ),
            F.avg("views").alias(
                "average_views"
            ),
        )
        .collect()[0]
    )

    return {
        "total_cars": total_cars,
        "cars_by_brand": {
            row["brand"]: row["count"]
            for row in cars_by_brand
        },
        "cars_by_fuel": {
            row["fuel"]: row["count"]
            for row in cars_by_fuel
        },
        "cars_by_transmission": {
            row["transmission"]: row["count"]
            for row in cars_by_transmission
        },
        "cars_by_condition": {
            row["condition"]: row["count"]
            for row in cars_by_condition
        },
        "average_mileage": (
            averages["average_mileage"]
        ),
        "average_price": (
            averages["average_price"]
        ),
        "average_price_difference_fipe_percent": (
            averages[
                "average_price_difference_fipe_percent"
            ]
        ),
        "average_views": (
            averages["average_views"]
        ),
    }