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

    return {
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
        "price_effective": (
            comparativo_preco.get("precoEfetivo")
        ),
        "price_fipe": (
            comparativo_preco.get("precoFipe")
        ),
        "price_market": (
            comparativo_preco.get("precoMercado")
        ),
        "price_difference_fipe_percent": (
            comparativo_preco.get(
                "percentualDiferencaFipe"
            )
        ),

        # Vendedor
        "seller_id": seller.get("id"),
        "seller_name": seller.get("nome"),

        # Métricas
        "views": car.get("visualizacoes"),

        # Datas
        "created_at": car.get("createdAt"),
        "updated_at": car.get("updatedAt"),
    }


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