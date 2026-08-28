from src.ingestion.cars import get_all_cars

from src.quality.cars import validate_cars

from src.storage.cars import (
    save_raw_cars,
    save_processed_cars,
)


def transform_car(
    car: dict,
) -> dict:
    """
    Transforma um veículo bruto da API
    em um registro estruturado para análise.
    """

    comparativo_preco = (
        car.get("comparativoPreco")
        or {}
    )

    seller = (
        car.get("seller")
        or {}
    )

    transformed_car = {

        # ========================================
        # IDENTIFICAÇÃO
        # ========================================

        "car_id": car.get("id"),

        # ========================================
        # INFORMAÇÕES DO VEÍCULO
        # ========================================

        "brand": car.get("marca"),

        "model": car.get("modelo"),

        "year": car.get("ano"),

        "color": car.get("cor"),

        "version": car.get("versao"),

        "mileage": car.get(
            "quilometragem"
        ),

        # ========================================
        # CARACTERÍSTICAS
        # ========================================

        "fuel": car.get(
            "combustivel"
        ),

        "transmission": car.get(
            "cambio"
        ),

        "body_type": car.get(
            "carroceria"
        ),

        # ========================================
        # STATUS
        # ========================================

        "status": car.get(
            "status"
        ),

        "condition": car.get(
            "condicao"
        ),

        # ========================================
        # PREÇOS
        # ========================================

        "price_effective": (
            comparativo_preco.get(
                "precoEfetivo"
            )
        ),

        "price_fipe": (
            comparativo_preco.get(
                "precoFipe"
            )
        ),

        "price_market": (
            comparativo_preco.get(
                "precoMercado"
            )
        ),

        "price_difference_fipe_percent": (
            comparativo_preco.get(
                "percentualDiferencaFipe"
            )
        ),

        # ========================================
        # VENDEDOR
        # ========================================

        "seller_id": seller.get(
            "id"
        ),

        "seller_name": seller.get(
            "nome"
        ),

        # ========================================
        # MÉTRICAS
        # ========================================

        "views": car.get(
            "visualizacoes"
        ),

        # ========================================
        # DATAS
        # ========================================

        "created_at": car.get(
            "createdAt"
        ),

        "updated_at": car.get(
            "updatedAt"
        ),
    }

    return transformed_car


def transform_cars(
    cars: list[dict],
) -> list[dict]:
    """
    Transforma uma lista de veículos.
    """

    return [
        transform_car(car)
        for car in cars
    ]


def main():

    print(
        "\n===== INICIANDO PIPELINE ====="
    )

    # ========================================
    # 1. INGESTION
    # ========================================

    print(
        "\n===== INGESTION ====="
    )

    cars = get_all_cars()

    print(
        f"Total de carros recebidos: "
        f"{len(cars)}"
    )

    # ========================================
    # 2. BRONZE
    # ========================================

    print(
        "\n===== SALVANDO BRONZE ====="
    )

    raw_file = save_raw_cars(
        {
            "data": cars,
        }
    )

    print(
        f"Bronze salvo em: {raw_file}"
    )

    # ========================================
    # 3. DATA QUALITY
    # ========================================

    print(
        "\n===== DATA QUALITY ====="
    )

    valid_cars, invalid_cars = (
        validate_cars(cars)
    )

    print(
        f"Registros válidos: "
        f"{len(valid_cars)}"
    )

    print(
        f"Registros inválidos: "
        f"{len(invalid_cars)}"
    )

    # ========================================
    # 4. TRANSFORMATION
    # ========================================

    print(
        "\n===== TRANSFORMATION ====="
    )

    transformed_cars = transform_cars(
        valid_cars
    )

    print(
        f"Total transformado: "
        f"{len(transformed_cars)}"
    )

    # ========================================
    # 5. SILVER
    # ========================================

    print(
        "\n===== SALVANDO SILVER ====="
    )

    processed_file = (
        save_processed_cars(
            transformed_cars
        )
    )

    print(
        f"Silver salvo em: "
        f"{processed_file}"
    )

    # ========================================
    # FINAL
    # ========================================

    print(
        "\n===== PIPELINE FINALIZADO "
        "COM SUCESSO =====\n"
    )


if __name__ == "__main__":
    main()