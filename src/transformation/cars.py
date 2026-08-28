from src.ingestion.client import VT3APIClient


def transform_car(car: dict) -> dict:
    """
    Transforma um veículo bruto da API
    em um registro estruturado para análise.
    """

    comparativo_preco = car.get("comparativoPreco") or {}
    seller = car.get("seller") or {}

    transformed_car = {
        # Identificação
        "car_id": car.get("id"),

        # Informações do veículo
        "brand": car.get("marca"),
        "model": car.get("modelo"),
        "year": car.get("ano"),
        "color": car.get("cor"),
        "version": car.get("versao"),
        "mileage": car.get("quilometragem"),

        # Características
        "fuel": car.get("combustivel"),
        "transmission": car.get("cambio"),
        "body_type": car.get("carroceria"),

        # Status
        "status": car.get("status"),
        "condition": car.get("condicao"),

        # Preços
        "price_effective": comparativo_preco.get(
            "precoEfetivo"
        ),
        "price_fipe": comparativo_preco.get(
            "precoFipe"
        ),
        "price_market": comparativo_preco.get(
            "precoMercado"
        ),
        "price_difference_fipe_percent": comparativo_preco.get(
            "percentualDiferencaFipe"
        ),

        # Informações do vendedor
        "seller_id": seller.get("id"),
        "seller_name": seller.get("nome"),

        # Métricas
        "views": car.get("visualizacoes"),

        # Datas
        "created_at": car.get("createdAt"),
        "updated_at": car.get("updatedAt"),
    }

    return transformed_car


def transform_cars(cars: list[dict]) -> list[dict]:
    """
    Transforma uma lista de veículos.
    """

    return [
        transform_car(car)
        for car in cars
    ]


def main():
    """
    Executa a transformação dos veículos.
    """

    print("\n===== INICIANDO TRANSFORMAÇÃO =====")

    # 1. Conecta à API
    client = VT3APIClient()

    # 2. Busca os dados
    response = client.get(
        "/cars",
        params={
            "page": 1,
            "limit": 100,
        },
    )

    # 3. Obtém a lista de carros
    if isinstance(response, dict):
        cars = response.get("data", [])
    else:
        cars = response

    print(
        f"\nTotal de carros recebidos: {len(cars)}"
    )

    # 4. Transforma os dados
    transformed_cars = transform_cars(cars)

    print(
        f"Total de carros transformados: "
        f"{len(transformed_cars)}"
    )

    # 5. Mostra um exemplo
    if transformed_cars:

        print(
            "\n===== EXEMPLO DE REGISTRO TRANSFORMADO =====\n"
        )

        for key, value in transformed_cars[0].items():

            print(f"{key}: {value}")

    print("\n===== TRANSFORMAÇÃO FINALIZADA =====\n")


if __name__ == "__main__":
    main()