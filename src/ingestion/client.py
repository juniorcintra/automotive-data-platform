import os

import requests
from dotenv import load_dotenv


load_dotenv()


class VT3APIClient:
    def __init__(self):
        self.base_url = os.getenv("API_BASE_URL")

        if not self.base_url:
            raise ValueError(
                "API_BASE_URL não encontrada nas variáveis de ambiente."
            )

    def get(
        self,
        endpoint: str,
        params: dict | None = None,
    ) -> dict:
        url = f"{self.base_url}{endpoint}"

        response = requests.get(
            url,
            params=params,
            timeout=30,
        )

        response.raise_for_status()

        return response.json()