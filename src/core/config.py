import os
from pathlib import Path

from dotenv import load_dotenv


BASE_DIR = (
    Path(__file__)
    .resolve()
    .parent
    .parent
    .parent
)

load_dotenv(
    BASE_DIR / ".env"
)

DATA_DIR = BASE_DIR / "data"

ENVIRONMENT = os.getenv(
    "ENVIRONMENT",
    "development",
)

LOG_LEVEL = os.getenv(
    "LOG_LEVEL",
    "INFO",
)

API_BASE_URL = os.getenv(
    "API_BASE_URL",
)

API_TIMEOUT = int(
    os.getenv(
        "API_TIMEOUT",
        "30",
    )
)

API_MAX_RETRIES = int(
    os.getenv(
        "API_MAX_RETRIES",
        "3",
    )
)

API_RETRY_DELAY = float(
    os.getenv(
        "API_RETRY_DELAY",
        "1",
    )
)