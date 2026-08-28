import json

from datetime import datetime
from pathlib import Path


DATA_DIR = Path("data")


def save_raw_cars(data: dict) -> Path:
    """
    Salva os dados brutos na camada Bronze.
    """

    timestamp = datetime.now().strftime(
        "%Y%m%d_%H%M%S"
    )

    output_dir = (
        DATA_DIR
        / "bronze"
        / "cars"
        / f"run_{timestamp}"
    )

    output_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    file_path = output_dir / "cars.json"

    with open(
        file_path,
        "w",
        encoding="utf-8",
    ) as file:
        json.dump(
            data,
            file,
            ensure_ascii=False,
            indent=2,
        )

    print(
        f"Dados brutos salvos em: {file_path}"
    )

    return file_path


def save_processed_cars(
    data: list[dict],
) -> Path:
    """
    Salva os dados transformados na camada Silver.
    """

    timestamp = datetime.now().strftime(
        "%Y%m%d_%H%M%S"
    )

    output_dir = (
        DATA_DIR
        / "silver"
        / "cars"
        / f"run_{timestamp}"
    )

    output_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    file_path = output_dir / "cars.json"

    with open(
        file_path,
        "w",
        encoding="utf-8",
    ) as file:
        json.dump(
            data,
            file,
            ensure_ascii=False,
            indent=2,
        )

    print(
        f"Dados processados salvos em: {file_path}"
    )

    return file_path