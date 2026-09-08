from pyspark.sql import DataFrame


def save_silver_cars(
    cars_df: DataFrame,
    output_path: str,
) -> str:
    """
    Salva o DataFrame Silver em formato Parquet.
    """

    (
        cars_df
        .write
        .mode("overwrite")
        .parquet(output_path)
    )

    return output_path