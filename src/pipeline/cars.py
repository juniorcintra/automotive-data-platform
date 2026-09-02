from datetime import datetime

from src.analytics.cars import (
    calculate_car_metrics,
)

from src.ingestion.cars import (
    get_all_cars,
)

from src.pipeline.metadata import (
    create_pipeline_metadata,
    fail_pipeline_metadata,
    finish_pipeline_metadata,
    save_pipeline_metadata,
    update_pipeline_stage,
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

    run_id = datetime.now().strftime(
        "run_%Y%m%d_%H%M%S"
    )

    metadata = create_pipeline_metadata(
        run_id
    )

    try:

        print(
            "\n===== INICIANDO PIPELINE ====="
        )

        print(
            f"Run ID: {run_id}"
        )

        # ========================================
        # 1. INGESTION
        # ========================================

        metadata = update_pipeline_stage(
            metadata=metadata,
            stage="ingestion",
        )

        print("\n===== INGESTION =====")

        cars = get_all_cars()

        print(
            f"Total de carros recebidos: "
            f"{len(cars)}"
        )

        # ========================================
        # 2. BRONZE
        # ========================================

        metadata = update_pipeline_stage(
            metadata=metadata,
            stage="bronze",
        )

        print("\n===== BRONZE =====")

        raw_file = save_raw_cars(
            data={
                "data": cars,
            },
            run_id=run_id,
        )

        print(
            f"Bronze salvo em: {raw_file}"
        )

        # ========================================
        # 3. DATA QUALITY
        # ========================================

        metadata = update_pipeline_stage(
            metadata=metadata,
            stage="data_quality",
        )

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

        metadata = update_pipeline_stage(
            metadata=metadata,
            stage="transformation",
        )

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

        metadata = update_pipeline_stage(
            metadata=metadata,
            stage="silver",
        )

        print("\n===== SILVER =====")

        processed_file = save_processed_cars(
            data=transformed_cars,
            run_id=run_id,
        )

        print(
            f"Silver salvo em: "
            f"{processed_file}"
        )

        # ========================================
        # 6. LOAD SILVER
        # ========================================

        metadata = update_pipeline_stage(
            metadata=metadata,
            stage="load_silver",
        )

        print("\n===== LOAD SILVER =====")

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

        metadata = update_pipeline_stage(
            metadata=metadata,
            stage="analytics",
        )

        print("\n===== GOLD / ANALYTICS =====")

        metrics = calculate_car_metrics(
            silver_cars
        )

        print(
            f"Total de carros analisados: "
            f"{metrics['total_cars']}"
        )

        # ========================================
        # 8. GOLD
        # ========================================

        metadata = update_pipeline_stage(
            metadata=metadata,
            stage="gold",
        )

        print("\n===== GOLD =====")

        gold_file = save_gold_metrics(
            metrics=metrics,
            run_id=run_id,
        )

        print(
            f"Gold salvo em: {gold_file}"
        )

        # ========================================
        # 9. FINALIZA METADATA
        # ========================================

        metadata = update_pipeline_stage(
            metadata=metadata,
            stage="completed",
        )

        metadata = finish_pipeline_metadata(
            metadata=metadata,
            total_received=len(cars),
            total_valid=len(valid_cars),
            total_invalid=len(invalid_cars),
            total_transformed=len(
                transformed_cars
            ),
        )

        save_pipeline_metadata(
            metadata
        )

        # ========================================
        # FINAL
        # ========================================

        print(
            "\n===== PIPELINE FINALIZADO "
            "COM SUCESSO =====\n"
        )

    except Exception as error:

        metadata = fail_pipeline_metadata(
            metadata=metadata,
            error=error,
        )

        save_pipeline_metadata(
            metadata
        )

        print(
            "\n===== PIPELINE FINALIZADO "
            "COM ERRO =====\n"
        )

        raise


if __name__ == "__main__":
    main()