import time

import requests

from src.core.config import (
    API_BASE_URL,
    API_MAX_RETRIES,
    API_RETRY_DELAY,
    API_TIMEOUT,
)

from src.core.logger import get_logger


logger = get_logger(
    __name__
)


class VT3APIClient:

    RETRYABLE_STATUS_CODES = {
        500,
        502,
        503,
        504,
    }

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

        total_attempts = API_MAX_RETRIES + 1

        for attempt in range(
            1,
            total_attempts + 1,
        ):

            logger.info(
                f"Realizando requisição GET: "
                f"{url} "
                f"(tentativa {attempt}/{total_attempts})"
            )

            try:

                response = requests.get(
                    url,
                    params=params,
                    timeout=API_TIMEOUT,
                )

                if (
                    response.status_code
                    in self.RETRYABLE_STATUS_CODES
                ):

                    if attempt < total_attempts:

                        logger.warning(
                            f"Erro HTTP transitório "
                            f"{response.status_code} "
                            f"na tentativa {attempt}/{total_attempts}. "
                            f"Tentando novamente em "
                            f"{API_RETRY_DELAY}s."
                        )

                        time.sleep(
                            API_RETRY_DELAY
                        )

                        continue

                response.raise_for_status()

                logger.info(
                    f"Requisição realizada com sucesso: "
                    f"{url}"
                )

                return response.json()

            except (
                requests.exceptions.Timeout,
                requests.exceptions.ConnectionError,
            ) as error:

                if attempt < total_attempts:

                    logger.warning(
                        f"{type(error).__name__} "
                        f"na tentativa "
                        f"{attempt}/{total_attempts}. "
                        f"Tentando novamente em "
                        f"{API_RETRY_DELAY}s."
                    )

                    time.sleep(
                        API_RETRY_DELAY
                    )

                    continue

                logger.exception(
                    f"Falha após "
                    f"{total_attempts} tentativas: "
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