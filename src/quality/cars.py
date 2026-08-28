from collections import Counter

from src.ingestion.client import VT3APIClient


def validate_car(car: dict) -> list[str]:
    """
    Executa regras de qualidade para um veículo.

    Retorna uma lista com os erros encontrados.
    Se a lista estiver vazia, o registro é considerado válido.
    """

    errors = []

    # ============================================================
    # ID
    # ============================================================

    car_id = car.get("id")

    if not car_id:
        errors.append("ID ausente")

    # ============================================================
    # MARCA
    # ============================================================

    brand = car.get("marca")

    if not brand or not str(brand).strip():
        errors.append("Marca ausente")

    # ============================================================
    # MODELO
    # ============================================================

    model = car.get("modelo")

    if not model or not str(model).strip():
        errors.append("Modelo ausente")

    # ============================================================
    # ANO
    # ============================================================

    year = car.get("ano")

    if year is None:
        errors.append("Ano ausente")

    else:
        try:
            year_value = int(year)

            if year_value < 1900 or year_value > 2030:
                errors.append(f"Ano inválido: {year}")

        except (ValueError, TypeError):
            errors.append(f"Ano inválido: {year}")

    # ============================================================
    # PREÇO EFETIVO
    # ============================================================

    price_data = car.get("comparativoPreco") or {}

    price = (
        car.get("precoEfetivo")
        or price_data.get("precoEfetivo")
    )

    if price is None:
        errors.append("Preço efetivo ausente")

    else:
        try:
            price_value = float(price)

            if price_value <= 0:
                errors.append(
                    f"Preço efetivo inválido: {price}"
                )

        except (ValueError, TypeError):
            errors.append(
                f"Preço efetivo inválido: {price}"
            )

    # ============================================================
    # QUILOMETRAGEM
    # ============================================================

    mileage = car.get("quilometragem")

    if mileage is not None:
        try:
            mileage_value = float(mileage)

            if mileage_value < 0:
                errors.append(
                    f"Quilometragem inválida: {mileage}"
                )

        except (ValueError, TypeError):
            errors.append(
                f"Quilometragem inválida: {mileage}"
            )

    return errors


def find_duplicate_ids(cars: list[dict]) -> list[str]:
    """
    Encontra IDs duplicados.
    """

    ids = [
        car.get("id")
        for car in cars
        if car.get("id")
    ]

    counter = Counter(ids)

    duplicate_ids = [
        car_id
        for car_id, count in counter.items()
        if count > 1
    ]

    return duplicate_ids


def main():
    """
    Executa a etapa de Data Quality
    para os veículos da API VT3.
    """

    print("\n===== INICIANDO DATA QUALITY =====")

    # ============================================================
    # 1. CONEXÃO COM A API
    # ============================================================

    client = VT3APIClient()

    # ============================================================
    # 2. EXTRAÇÃO DOS DADOS
    # ============================================================

    response = client.get(
        "/cars",
        params={
            "page": 1,
            "limit": 100,
        },
    )

    # ============================================================
    # 3. OBTÉM A LISTA DE VEÍCULOS
    # ============================================================

    if isinstance(response, dict):
        cars = response.get("data", [])
    else:
        cars = response

    print(f"\nTotal de carros recebidos: {len(cars)}")

    # ============================================================
    # 4. VALIDA OS REGISTROS
    # ============================================================

    invalid_cars = []

    total_errors = 0

    for car in cars:

        errors = validate_car(car)

        if errors:

            invalid_cars.append(
                {
                    "id": car.get("id"),
                    "marca": car.get("marca"),
                    "modelo": car.get("modelo"),
                    "errors": errors,
                }
            )

            total_errors += len(errors)

    # ============================================================
    # 5. PROCURA DUPLICIDADES
    # ============================================================

    duplicate_ids = find_duplicate_ids(cars)

    # ============================================================
    # 6. MONTA O RELATÓRIO
    # ============================================================

    report = {
        "total_records": len(cars),
        "valid_records": len(cars) - len(invalid_cars),
        "invalid_records": len(invalid_cars),
        "total_validation_errors": total_errors,
        "duplicate_ids": duplicate_ids,
        "invalid_cars": invalid_cars,
    }

    # ============================================================
    # 7. EXIBE O RELATÓRIO
    # ============================================================

    print("\n===== DATA QUALITY REPORT =====")

    print(
        f"Total de registros: "
        f"{report['total_records']}"
    )

    print(
        f"Registros válidos: "
        f"{report['valid_records']}"
    )

    print(
        f"Registros inválidos: "
        f"{report['invalid_records']}"
    )

    print(
        f"Erros encontrados: "
        f"{report['total_validation_errors']}"
    )

    print(
        f"IDs duplicados: "
        f"{len(report['duplicate_ids'])}"
    )

    print("================================")

    # ============================================================
    # 8. EXIBE EXEMPLOS DE REGISTROS INVÁLIDOS
    # ============================================================

    if invalid_cars:

        print(
            "\n===== EXEMPLOS DE REGISTROS INVÁLIDOS ====="
        )

        for invalid_car in invalid_cars[:5]:

            print(
                f"\nCarro ID: "
                f"{invalid_car['id']}"
            )

            print(
                f"Veículo: "
                f"{invalid_car['marca']} "
                f"{invalid_car['modelo']}"
            )

            for error in invalid_car["errors"]:

                print(f"  - {error}")

    else:

        print(
            "\nNenhum registro inválido encontrado."
        )

    # ============================================================
    # 9. EXIBE DUPLICIDADES
    # ============================================================

    if duplicate_ids:

        print("\n===== IDs DUPLICADOS =====")

        for car_id in duplicate_ids:

            print(f"ID duplicado: {car_id}")

    print("\n===== DATA QUALITY FINALIZADO =====\n")


if __name__ == "__main__":
    main()