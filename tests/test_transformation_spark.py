from pyspark.sql import SparkSession
from pyspark.sql.types import (
    ArrayType,
    DoubleType,
    IntegerType,
    StringType,
    StructField,
    StructType,
)

from src.transformation.cars_spark import (
    transform_cars_spark,
)


def create_test_spark_session():
    return (
        SparkSession.builder
        .master("local[2]")
        .appName("automotive-data-platform-tests")
        .getOrCreate()
    )


def test_transform_cars_spark():
    spark = create_test_spark_session()

    comparativo_preco_schema = StructType(
        [
            StructField(
                "precoEfetivo",
                DoubleType(),
                True,
            ),
            StructField(
                "precoFipe",
                DoubleType(),
                True,
            ),
            StructField(
                "mediaMercado",
                DoubleType(),
                True,
            ),
            StructField(
                "percentualDiferencaFipe",
                DoubleType(),
                True,
            ),
        ]
    )

    seller_schema = StructType(
        [
            StructField(
                "id",
                StringType(),
                True,
            ),
            StructField(
                "nome",
                StringType(),
                True,
            ),
        ]
    )

    car_schema = StructType(
        [
            StructField(
                "id",
                StringType(),
                True,
            ),
            StructField(
                "marca",
                StringType(),
                True,
            ),
            StructField(
                "modelo",
                StringType(),
                True,
            ),
            StructField(
                "ano",
                IntegerType(),
                True,
            ),
            StructField(
                "cor",
                StringType(),
                True,
            ),
            StructField(
                "versao",
                StringType(),
                True,
            ),
            StructField(
                "quilometragem",
                DoubleType(),
                True,
            ),
            StructField(
                "combustivel",
                StringType(),
                True,
            ),
            StructField(
                "cambio",
                StringType(),
                True,
            ),
            StructField(
                "carroceria",
                StringType(),
                True,
            ),
            StructField(
                "status",
                StringType(),
                True,
            ),
            StructField(
                "condicao",
                StringType(),
                True,
            ),
            StructField(
                "comparativoPreco",
                comparativo_preco_schema,
                True,
            ),
            StructField(
                "seller",
                seller_schema,
                True,
            ),
            StructField(
                "visualizacoes",
                IntegerType(),
                True,
            ),
            StructField(
                "createdAt",
                StringType(),
                True,
            ),
            StructField(
                "updatedAt",
                StringType(),
                True,
            ),
        ]
    )

    schema = StructType(
        [
            StructField(
                "data",
                ArrayType(car_schema),
                True,
            )
        ]
    )

    data = [
        {
            "id": "1",
            "marca": "Nissan",
            "modelo": "Tiida",
            "ano": 2013,
            "cor": "Cinza",
            "versao": "SL",
            "quilometragem": 140000.0,
            "combustivel": "Flex",
            "cambio": "Manual",
            "carroceria": "Hatchback",
            "status": "disponivel",
            "condicao": "usado",
            "comparativoPreco": {
                "precoEfetivo": 40000.0,
                "precoFipe": 42000.0,
                "mediaMercado": 41000.0,
                "percentualDiferencaFipe": -4.76,
            },
            "seller": {
                "id": "seller-1",
                "nome": "VT3 Automóveis",
            },
            "visualizacoes": 100,
            "createdAt": "2026-08-01T10:00:00.000Z",
            "updatedAt": "2026-08-02T10:00:00.000Z",
        }
    ]

    try:
        cars_df = spark.createDataFrame(
            [(data,)],
            schema=schema,
        )

        result = transform_cars_spark(
            cars_df
        )

        assert result.count() == 1

        row = result.first()

        assert row.car_id == "1"
        assert row.brand == "Nissan"
        assert row.model == "Tiida"
        assert row.year == 2013
        assert row.mileage == 140000.0
        assert row.price_effective == 40000.0
        assert row.price_fipe == 42000.0
        assert row.price_market_average == 41000.0
        assert row.seller_name == "VT3 Automóveis"

    finally:
        spark.stop()