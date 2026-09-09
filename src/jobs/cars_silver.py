from src.storage.cars_spark import save_silver_cars
from src.transformation.cars_spark import (
    create_spark_session,
    read_bronze_cars,
    transform_cars_spark,
)


def run_silver_job(
    input_path: str,
    output_path: str,
) -> str:
    """
    Executa o processamento Bronze -> Silver
    utilizando PySpark.
    """

    spark = create_spark_session()

    try:
        cars_df = read_bronze_cars(
            spark,
            input_path,
        )

        cars_silver = transform_cars_spark(
            cars_df
        )

        return save_silver_cars(
            cars_silver,
            output_path,
        )

    finally:
        spark.stop()