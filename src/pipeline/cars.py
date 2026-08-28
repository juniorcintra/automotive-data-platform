from src.analytics.cars import (
    calculate_car_metrics,
)

from src.ingestion.cars import (
    get_all_cars,
)

from src.quality.cars import (
    validate_cars,
)

from src.storage.cars import (
    load_processed_cars,
    save_gold_metrics,
    save_processed_cars,
    save_raw_cars,
)

from src.transformation.cars import (
    transform_cars,
)


def main():
    """
    Executa o pipeline completo de veículos.
    """

    print(
        "\n===== INICIANDO PIPELINE ====="
    )

    # ========================================
    # 1. INGESTION
    # ========================================

    print("\n===== INGESTION =====")

    cars = get_all_cars()

    print(
        f"Total de carros recebidos: "
        f"{len(cars)}"
    )

    # ========================================
    # 2. BRONZE
    # ========================================

    print("\n===== BRONZE =====")

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

    print("\n===== DATA QUALITY =====")

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

    print("\n===== TRANSFORMATION =====")

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

    print("\n===== SILVER =====")

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
    # 6. CARREGA SILVER
    # ========================================

    silver_cars = load_processed_cars(
        processed_file
    )

    print(
        f"Registros carregados da Silver: "
        f"{len(silver_cars)}"
    )

    # ========================================
    # 7. GOLD / ANALYTICS
    # ========================================

    print("\n===== GOLD / ANALYTICS =====")

    metrics = calculate_car_metrics(
        silver_cars
    )

    print(
        f"Total de carros analisados: "
        f"{metrics['total_cars']}"
    )

    # ========================================
    # 8. SALVA GOLD
    # ========================================

    gold_file = save_gold_metrics(
        metrics
    )

    print(
        f"Gold salvo em: {gold_file}"
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