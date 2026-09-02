import json

from datetime import datetime

from pathlib import Path


DATA_DIR = Path("data")


def create_pipeline_metadata(
    run_id: str,
) -> dict:
    """
    Cria os metadados iniciais
    de uma execução do pipeline.
    """

    return {
        "run_id": run_id,
        "status": "running",
        "started_at": datetime.now().isoformat(),
        "finished_at": None,
        "total_received": 0,
        "total_valid": 0,
        "total_invalid": 0,
        "total_transformed": 0,
        "error": None,
        "duration_seconds": None,
    }

def calculate_pipeline_duration(
    started_at: str,
    finished_at: str,
) -> float:
    """
    Calcula a duração da execução
    do pipeline em segundos.
    """

    started_datetime = datetime.fromisoformat(
        started_at
    )

    finished_datetime = datetime.fromisoformat(
        finished_at
    )

    duration = (
        finished_datetime
        - started_datetime
    )

    return duration.total_seconds()


def finish_pipeline_metadata(
    metadata: dict,
    total_received: int,
    total_valid: int,
    total_invalid: int,
    total_transformed: int,
) -> dict:
    """
    Finaliza os metadados
    de uma execução do pipeline.
    """

    metadata["status"] = "success"

    metadata["finished_at"] = (
        datetime.now().isoformat()
    )

    metadata["duration_seconds"] = (
        calculate_pipeline_duration(
            started_at=metadata["started_at"],
            finished_at=metadata["finished_at"],
        )
    )

    metadata["total_received"] = total_received

    metadata["total_valid"] = total_valid

    metadata["total_invalid"] = total_invalid

    metadata["total_transformed"] = (
        total_transformed
    )

    return metadata


def save_pipeline_metadata(
    metadata: dict,
) -> Path:
    """
    Salva os metadados da execução
    do pipeline em arquivo JSON.
    """

    run_id = metadata["run_id"]

    output_dir = (
        DATA_DIR
        / "metadata"
        / run_id
    )

    output_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    file_path = (
        output_dir
        / "metadata.json"
    )

    with open(
        file_path,
        "w",
        encoding="utf-8",
    ) as file:

        json.dump(
            metadata,
            file,
            ensure_ascii=False,
            indent=2,
        )

    print(
        f"Metadata salvo em: {file_path}"
    )

    return file_path

def fail_pipeline_metadata(
    metadata: dict,
    error: Exception,
) -> dict:
    """
    Registra a falha de uma execução
    do pipeline.
    """

    metadata["status"] = "failed"

    metadata["finished_at"] = (
        datetime.now().isoformat()
    )

    metadata["duration_seconds"] = (
        calculate_pipeline_duration(
            started_at=metadata["started_at"],
            finished_at=metadata["finished_at"],
        )
    )

    metadata["error"] = str(error)

    return metadata