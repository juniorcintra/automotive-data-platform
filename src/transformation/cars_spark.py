from pyspark.sql import DataFrame
from pyspark.sql import functions as F
from pyspark.sql import SparkSession


def create_spark_session() -> SparkSession:
    """
    Cria a SparkSession da aplicação.
    """

    return (
        SparkSession.builder
        .appName("automotive-data-platform")
        .getOrCreate()
    )


def read_bronze_cars(
    spark: SparkSession,
    file_path: str,
) -> DataFrame:
    """
    Lê os dados Bronze de veículos em JSON.
    """

    return (
        spark.read
        .option("multiLine", "true")
        .json(file_path)
    )


def transform_cars_spark(
    cars_df: DataFrame,
) -> DataFrame:
    """
    Transforma os dados de veículos usando PySpark.

    Normaliza o array data, extrai campos simples
    e nested fields e realiza conversões de tipos.
    """

    return (
        cars_df
        .select(
            F.explode("data").alias("car")
        )
        .select(
            F.col("car.id").alias("car_id"),
            F.col("car.marca").alias("brand"),
            F.col("car.modelo").alias("model"),
            F.col("car.ano").cast("integer").alias("year"),
            F.col("car.cor").alias("color"),
            F.col("car.versao").alias("version"),
            F.col("car.quilometragem")
            .cast("double")
            .alias("mileage"),
            F.col("car.combustivel").alias("fuel"),
            F.col("car.cambio").alias("transmission"),
            F.col("car.carroceria").alias("body_type"),
            F.col("car.status").alias("status"),
            F.col("car.condicao").alias("condition"),

            F.col(
                "car.comparativoPreco.precoEfetivo"
            )
            .cast("double")
            .alias("price_effective"),

            F.col(
                "car.comparativoPreco.precoFipe"
            )
            .cast("double")
            .alias("price_fipe"),

            F.col(
                "car.comparativoPreco.mediaMercado"
            )
            .cast("double")
            .alias("price_market_average"),

            F.col(
                "car.comparativoPreco.percentualDiferencaFipe"
            )
            .cast("double")
            .alias(
                "price_difference_fipe_percent"
            ),

            F.col(
                "car.seller.id"
            ).alias("seller_id"),

            F.col(
                "car.seller.nome"
            ).alias("seller_name"),

            F.col(
                "car.visualizacoes"
            )
            .cast("integer")
            .alias("views"),

            F.to_timestamp(
                "car.createdAt"
            ).alias("created_at"),

            F.to_timestamp(
                "car.updatedAt"
            ).alias("updated_at"),
        )
    )