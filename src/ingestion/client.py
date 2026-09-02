import requests

from src.core.config import (
    API_BASE_URL,
    API_TIMEOUT,
)

from src.core.logger import get_logger


logger = get_logger(__name__)


class VT3APIClient:

    def __init__(self):

        self.base_url = API_BASE_URL

        if not self.base_url:

            raise ValueError(
                "API_BASE_URL não encontrada nas variáveis "
                "de ambiente."
            )

    def get(
        self,
        endpoint: str,
        params: dict | None = None,
    ) -> dict:

        url = f"{self.base_url}{endpoint}"

        logger.info(
            f"Realizando requisição GET: {url}"
        )

        try:

            response = requests.get(
                url,
                params=params,
                timeout=API_TIMEOUT,
            )

            response.raise_for_status()

            logger.info(
                f"Requisição realizada com sucesso: "
                f"{url}"
            )

            return response.json()

        except requests.exceptions.Timeout:

            logger.exception(
                f"Timeout ao realizar requisição: "
                f"{url}"
            )

            raise

        except requests.exceptions.ConnectionError:

            logger.exception(
                f"Erro de conexão ao realizar requisição: "
                f"{url}"
            )

            raise

        except requests.exceptions.HTTPError:

            logger.exception(
                f"Erro HTTP ao realizar requisição: "
                f"{url}"
            )

            raise

        except requests.exceptions.RequestException:

            logger.exception(
                f"Erro ao realizar requisição: "
                f"{url}"
            )

            raise