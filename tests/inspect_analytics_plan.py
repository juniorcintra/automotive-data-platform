from src.analytics.cars_spark import (
    calculate_car_metrics_spark,
)
from src.transformation.cars_spark import (
    create_spark_session,
)


def main():
    spark = create_spark_session()

    try:
        cars_df = spark.createDataFrame(
            [
                (
                    "1",
                    "Toyota",
                    "Flex",
                    "Automático",
                    "Usado",
                    45000.0,
                    120000.0,
                    -3.0,
                    150,
                ),
                (
                    "2",
                    "Toyota",
                    "Flex",
                    "Automático",
                    "Usado",
                    30000.0,
                    100000.0,
                    -4.0,
                    100,
                ),
                (
                    "3",
                    "Honda",
                    "Flex",
                    "Manual",
                    "Usado",
                    60000.0,
                    140000.0,
                    -3.5,
                    200,
                ),
            ],
            [
                "car_id",
                "brand",
                "fuel",
                "transmission",
                "condition",
                "mileage",
                "price_effective",
                "price_difference_fipe_percent",
                "views",
            ],
        )

        print("\n=== DATAFRAME ===")
        cars_df.show()

        print("\n=== PLANO: GROUP BY BRAND ===")
        (
            cars_df
            .groupBy("brand")
            .count()
            .explain("formatted")
        )

        print("\n=== PLANO: MÉDIAS ===")
        (
            cars_df
            .agg(
                {"mileage": "avg"}
            )
            .explain("formatted")
        )

        print("\n=== EXECUTANDO ANALYTICS ===")
        metrics = calculate_car_metrics_spark(cars_df)

        print("\n=== RESULTADO ===")
        print(metrics)

    finally:
        spark.stop()


if __name__ == "__main__":
    main()