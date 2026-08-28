from pyspark.sql import SparkSession


def get_spark_session() -> SparkSession:
    """
    Cria ou reutiliza uma SparkSession.
    """

    return (
        SparkSession.builder
        .appName("vt3-data-pipeline")
        .master("local[*]")
        .getOrCreate()
    )