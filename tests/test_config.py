from pathlib import Path

from src.core.config import (
    BASE_DIR,
    DATA_DIR,
    API_TIMEOUT
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