from pathlib import Path

from src.core.config import (
    BASE_DIR,
    DATA_DIR,
    API_TIMEOUT,
    API_MAX_RETRIES,
    API_RETRY_DELAY,
)


def test_base_dir_exists():

    assert BASE_DIR.exists()

    assert BASE_DIR.is_dir()


def test_data_dir_is_inside_base_dir():

    assert DATA_DIR == (
        BASE_DIR / "data"
    )


def test_data_dir_is_path():

    assert isinstance(
        DATA_DIR,
        Path,
    )

def test_api_timeout_is_integer():

    assert isinstance(
        API_TIMEOUT,
        int,
    )

    assert API_TIMEOUT > 0

def test_api_max_retries():
    assert API_MAX_RETRIES == 3


def test_api_retry_delay():
    assert API_RETRY_DELAY == 1