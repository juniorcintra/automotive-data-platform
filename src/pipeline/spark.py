import subprocess
from pathlib import Path

from src.core.config import BASE_DIR, DATA_DIR
from src.core.logger import get_logger


logger = get_logger(__name__)


def _to_container_path(file_path: Path) -> str:
    """
    Converte um caminho local do projeto para o caminho
    equivalente dentro do container Spark.
    """

    file_path = Path(file_path)

    if not file_path.is_absolute():
        file_path = BASE_DIR / file_path

    file_path = file_path.resolve()
    data_dir = DATA_DIR.resolve()

    relative_path = file_path.relative_to(data_dir)

    return f"/app/data/{relative_path.as_posix()}"


def run_silver_spark_job(
    input_path: Path,
    output_path: Path,
    run_id: str,
) -> Path:
    """
    Executa o Spark Silver Job através do Docker Compose.
    """

    container_input = _to_container_path(input_path)
    container_output = _to_container_path(output_path)

    command = [
        "docker",
        "compose",
        "exec",
        "-T",
        "spark",
        "/opt/spark/bin/spark-submit",
        "src/jobs/cars_silver.py",
        "--input",
        container_input,
        "--output",
        container_output,
        "--run-id",
        run_id,
    ]

    logger.info(
        "Executando Spark Silver Job | run_id=%s",
        run_id,
    )

    logger.info(
        "Spark input: %s | run_id=%s",
        container_input,
        run_id,
    )

    logger.info(
        "Spark output: %s | run_id=%s",
        container_output,
        run_id,
    )

    subprocess.run(
        command,
        cwd=BASE_DIR,
        check=True,
    )

    logger.info(
        "Spark Silver Job concluído | run_id=%s",
        run_id,
    )

    return output_path