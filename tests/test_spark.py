from src.spark.session import (
    get_spark_session,
)


def test_create_spark_session():

    spark = get_spark_session()

    assert spark is not None

    assert spark.sparkContext is not None