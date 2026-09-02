import json

from pathlib import Path

import pandas as pd


from src.core.config import DATA_DIR


def save_raw_cars(
    data: dict,
    run_id: str,
) -> Path:
    """
    Salva os dados brutos na camada Bronze.
    """

    output_dir = (
        DATA_DIR
        / "bronze"
        / "cars"
        / run_id
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
        f"Dados Bronze salvos em: {file_path}"
    )

    return file_path


def save_processed_cars(
    data: list[dict],
    run_id: str,
) -> Path:
    """
    Salva os dados processados
    na camada Silver em formato Parquet.
    """

    output_dir = (
        DATA_DIR
        / "silver"
        / "cars"
        / run_id
    )

    output_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    file_path = (
        output_dir
        / "cars.parquet"
    )

    dataframe = pd.DataFrame(
        data
    )

    dataframe.to_parquet(
        file_path,
        index=False,
        engine="pyarrow",
    )

    print(
        f"Dados Silver salvos em: {file_path}"
    )

    return file_path


def load_processed_cars(
    file_path: Path,
) -> list[dict]:
    """
    Carrega os veículos da camada Silver
    armazenados em formato Parquet.
    """

    dataframe = pd.read_parquet(
        file_path,
        engine="pyarrow",
    )

    return dataframe.to_dict(
        orient="records"
    )


def save_gold_metrics(
    metrics: dict,
    run_id: str,
) -> Path:
    """
    Salva as métricas agregadas
    na camada Gold.
    """

    output_dir = (
        DATA_DIR
        / "gold"
        / "cars"
        / run_id
    )

    output_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    file_path = (
        output_dir
        / "cars_metrics.json"
    )

    with open(
        file_path,
        "w",
        encoding="utf-8",
    ) as file:
        json.dump(
            metrics,
            file,
            ensure_ascii=False,
            indent=2,
        )

    print(
        f"Dados Gold salvos em: {file_path}"
    )

    return file_path