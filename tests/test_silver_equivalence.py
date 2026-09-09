import json
from datetime import datetime

from src.transformation.cars import (
    transform_cars,
)
from src.transformation.cars_spark import (
    create_spark_session,
    transform_cars_spark,
)


def normalize_value(value):
    """
    Normaliza valores para permitir comparação entre
    Python Silver e Spark Silver.
    """
    if isinstance(value, datetime):
        return value.isoformat()

    return value


def normalize_record(record):
    """
    Normaliza um registro Silver para comparação.
    """
    return {
        key: normalize_value(value)
        for key, value in record.items()
    }


def test_python_and_spark_silver_are_equivalent(
    tmp_path,
):
    raw_cars = [
        {
            "id": "car-001",
            "marca": "Toyota",
            "modelo": "Corolla",
            "ano": 2022,
            "cor": "Prata",
            "versao": "2.0 XEi",
            "quilometragem": 45000,
            "combustivel": "Flex",
            "cambio": "Automático",
            "carroceria": "Sedan",
            "status": "Disponível",
            "condicao": "Usado",
            "comparativoPreco": {
                "precoEfetivo": 119900,
                "precoFipe": 125000,
                "mediaMercado": 123000,
                "percentualDiferencaFipe": -4.08,
            },
            "seller": {
                "id": "seller-001",
                "nome": "VT3 Automóveis",
            },
            "visualizacoes": 150,
            "createdAt": "2026-09-02T10:00:00",
            "updatedAt": "2026-09-02T11:00:00",
        }
    ]

    python_silver = transform_cars(
        raw_cars
    )

    spark = create_spark_session()

    try:
        raw_json_path = (
            tmp_path / "cars.json"
        )

        raw_json_path.write_text(
            json.dumps(
                {
                    "data": raw_cars,
                }
            ),
            encoding="utf-8",
        )

        raw_df = (
            spark.read
            .option("multiLine", "true")
            .json(str(raw_json_path))
        )

        spark_silver_df = transform_cars_spark(
            raw_df
        )

        spark_silver = [
            row.asDict()
            for row in spark_silver_df.collect()
        ]

    finally:
        spark.stop()

    assert len(python_silver) == 1
    assert len(spark_silver) == 1

    python_record = normalize_record(
        python_silver[0]
    )

    spark_record = normalize_record(
        spark_silver[0]
    )

    assert python_record == spark_record