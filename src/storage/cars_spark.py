from pathlib import Path

from pyspark.sql import DataFrame
from pyspark.sql import SparkSession


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


def load_silver_cars(
    spark: SparkSession,
    input_path: str | Path,
) -> list[dict]:
    """
    Carrega a Silver Spark em Parquet e retorna
    os registros como uma lista de dicionários.
    """
    input_path = Path(input_path)

    cars_df = (
        spark.read
        .parquet(input_path.as_posix())
    )

    return [
        row.asDict()
        for row in cars_df.collect()
    ]