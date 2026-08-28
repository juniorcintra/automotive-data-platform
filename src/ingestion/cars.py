import json
from datetime import datetime
from pathlib import Path

from src.ingestion.client import VT3APIClient


def save_raw_data(data: dict, page: int, output_dir: Path):
    file_path = output_dir / f"page_{page}.json"

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

    print(f"Página {page} salva em: {file_path}")


def main():
    client = VT3APIClient()

    response = client.get(
        "/cars",
        params={
            "page": 1,
            "limit": 10,
        },
    )

    total_pages = response["meta"]["totalPages"]

    print(f"Total de páginas: {total_pages}")

    run_timestamp = datetime.now().strftime(
        "%Y%m%d_%H%M%S"
    )

    output_dir = Path(
        "data"
    ) / "bronze" / "cars" / f"run_{run_timestamp}"

    output_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    save_raw_data(
        data=response,
        page=1,
        output_dir=output_dir,
    )

    for page in range(2, total_pages + 1):
        print(f"Buscando página {page}...")

        response = client.get(
            "/cars",
            params={
                "page": page,
                "limit": 10,
            },
        )

        save_raw_data(
            data=response,
            page=page,
            output_dir=output_dir,
        )

    print("\nIngestão concluída com sucesso!")


if __name__ == "__main__":
    main()