from datetime import datetime


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
    }


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

    metadata["total_received"] = total_received

    metadata["total_valid"] = total_valid

    metadata["total_invalid"] = total_invalid

    metadata["total_transformed"] = (
        total_transformed
    )

    return metadata