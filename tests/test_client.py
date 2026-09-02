from unittest.mock import Mock, patch

import pytest
import requests

from src.ingestion.client import VT3APIClient


def test_client_raises_error_without_api_base_url():

    with patch(
        "src.ingestion.client.API_BASE_URL",
        None,
    ):

        with pytest.raises(
            ValueError,
            match="API_BASE_URL não encontrada",
        ):

            VT3APIClient()


def test_client_initializes_with_api_base_url():

    with patch(
        "src.ingestion.client.API_BASE_URL",
        "https://api.example.com",
    ):

        client = VT3APIClient()

    assert client.base_url == (
        "https://api.example.com"
    )


def test_client_get_returns_json():

    response_data = {
        "data": [
            {
                "id": "1",
                "marca": "Toyota",
            }
        ]
    }

    mock_response = Mock()

    mock_response.json.return_value = (
        response_data
    )

    with (
        patch(
            "src.ingestion.client.API_BASE_URL",
            "https://api.example.com",
        ),
        patch(
            "src.ingestion.client.requests.get",
            return_value=mock_response,
        ) as mock_get,
    ):

        client = VT3APIClient()

        result = client.get(
            "/cars"
        )

    mock_get.assert_called_once_with(
        "https://api.example.com/cars",
        params=None,
        timeout=30,
    )

    mock_response.raise_for_status.assert_called_once()

    assert result == response_data


def test_client_get_passes_params():

    mock_response = Mock()

    mock_response.json.return_value = {
        "data": []
    }

    params = {
        "page": 1,
        "limit": 10,
    }

    with (
        patch(
            "src.ingestion.client.API_BASE_URL",
            "https://api.example.com",
        ),
        patch(
            "src.ingestion.client.requests.get",
            return_value=mock_response,
        ) as mock_get,
    ):

        client = VT3APIClient()

        client.get(
            "/cars",
            params=params,
        )

    mock_get.assert_called_once_with(
        "https://api.example.com/cars",
        params=params,
        timeout=30,
    )


def test_client_logs_and_raises_timeout():

    error = requests.exceptions.Timeout(
        "Request timed out"
    )

    with (
        patch(
            "src.ingestion.client.API_BASE_URL",
            "https://api.example.com",
        ),
        patch(
            "src.ingestion.client.requests.get",
            side_effect=error,
        ),
        patch(
            "src.ingestion.client.logger.exception",
        ) as mock_logger_exception,
    ):

        client = VT3APIClient()

        with pytest.raises(
            requests.exceptions.Timeout,
        ):

            client.get(
                "/cars"
            )

    mock_logger_exception.assert_called_once()


def test_client_logs_and_raises_connection_error():

    error = requests.exceptions.ConnectionError(
        "Connection failed"
    )

    with (
        patch(
            "src.ingestion.client.API_BASE_URL",
            "https://api.example.com",
        ),
        patch(
            "src.ingestion.client.requests.get",
            side_effect=error,
        ),
        patch(
            "src.ingestion.client.logger.exception",
        ) as mock_logger_exception,
    ):

        client = VT3APIClient()

        with pytest.raises(
            requests.exceptions.ConnectionError,
        ):

            client.get(
                "/cars"
            )

    mock_logger_exception.assert_called_once()


def test_client_logs_and_raises_http_error():

    error = requests.exceptions.HTTPError(
        "Internal Server Error"
    )

    mock_response = Mock()

    mock_response.raise_for_status.side_effect = (
        error
    )

    with (
        patch(
            "src.ingestion.client.API_BASE_URL",
            "https://api.example.com",
        ),
        patch(
            "src.ingestion.client.requests.get",
            return_value=mock_response,
        ),
        patch(
            "src.ingestion.client.logger.exception",
        ) as mock_logger_exception,
    ):

        client = VT3APIClient()

        with pytest.raises(
            requests.exceptions.HTTPError,
        ):

            client.get(
                "/cars"
            )

    mock_logger_exception.assert_called_once()


def test_client_logs_and_raises_request_exception():

    error = requests.exceptions.RequestException(
        "Generic request error"
    )

    with (
        patch(
            "src.ingestion.client.API_BASE_URL",
            "https://api.example.com",
        ),
        patch(
            "src.ingestion.client.requests.get",
            side_effect=error,
        ),
        patch(
            "src.ingestion.client.logger.exception",
        ) as mock_logger_exception,
    ):

        client = VT3APIClient()

        with pytest.raises(
            requests.exceptions.RequestException,
        ):

            client.get(
                "/cars"
            )

    mock_logger_exception.assert_called_once()