from datetime import datetime
from time import perf_counter

from src.core.logger import get_logger
from src.storage.cars_spark import save_silver_cars
from src.transformation.cars_spark import (
    create_spark_session,
    read_bronze_cars,
    transform_cars_spark,
)


logger = get_logger(__name__)


def run_silver_job(
    input_path: str,
    output_path: str,
    run_id: str | None = None,
) -> str:
    """
    Executa o processamento Bronze -> Silver
    utilizando PySpark.

    Registra informações de execução através de run_id,
    logs de etapas e duração total do job.
    """

    run_id = run_id or datetime.now().strftime(
        "run_%Y%m%d_%H%M%S"
    )

    started_at = perf_counter()

    logger.info(
        "Job Bronze -> Silver iniciado | run_id=%s",
        run_id,
    )
    logger.info(
        "Input Bronze: %s | run_id=%s",
        input_path,
        run_id,
    )

    spark = create_spark_session()

    try:
        logger.info(
            "Lendo Bronze | run_id=%s",
            run_id,
        )

        cars_df = read_bronze_cars(
            spark,
            input_path,
        )

        logger.info(
            "Bronze carregado | run_id=%s",
            run_id,
        )

        logger.info(
            "Iniciando transformação Bronze -> Silver | run_id=%s",
            run_id,
        )

        cars_silver = transform_cars_spark(
            cars_df
        )

        logger.info(
            "Transformação concluída | run_id=%s",
            run_id,
        )

        logger.info(
            "Salvando Silver: %s | run_id=%s",
            output_path,
            run_id,
        )

        result = save_silver_cars(
            cars_silver,
            output_path,
        )

        duration = perf_counter() - started_at

        logger.info(
            "Job Bronze -> Silver concluído com sucesso | "
            "run_id=%s | duration=%.2fs",
            run_id,
            duration,
        )

        return result

    except Exception:
        duration = perf_counter() - started_at

        logger.exception(
            "Job Bronze -> Silver falhou | "
            "run_id=%s | duration=%.2fs",
            run_id,
            duration,
        )

        raise

    finally:
        spark.stop()

        logger.info(
            "SparkSession encerrada | run_id=%s",
            run_id,
        )


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Executa o job Bronze -> Silver com PySpark."
    )

    parser.add_argument(
        "--input",
        required=True,
        help="Caminho do arquivo Bronze JSON.",
    )

    parser.add_argument(
        "--output",
        required=True,
        help="Caminho do diretório de saída Silver.",
    )

    parser.add_argument(
        "--run-id",
        required=False,
        help="Identificador da execução.",
    )

    args = parser.parse_args()

    run_silver_job(
        input_path=args.input,
        output_path=args.output,
        run_id=args.run_id,
    )