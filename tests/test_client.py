from unittest.mock import patch

import pytest
import requests

from src.ingestion.client import VT3APIClient


def test_client_without_api_base_url():

    with patch(
        "src.ingestion.client.API_BASE_URL",
        None,
    ):

        try:
            VT3APIClient()
            assert False
        except ValueError as error:
            assert (
                str(error)
                == "API_BASE_URL não encontrada nas variáveis "
                "de ambiente."
            )


def test_client_initializes_with_api_base_url():

    with patch(
        "src.ingestion.client.API_BASE_URL",
        "https://api.example.com",
    ):

        client = VT3APIClient()

    assert (
        client.base_url
        == "https://api.example.com"
    )


def test_get_returns_json():

    client = VT3APIClient()

    response = type(
        "Response",
        (),
        {
            "status_code": 200,
            "raise_for_status": lambda self: None,
            "json": lambda self: {
                "data": []
            },
        },
    )()

    with patch(
        "src.ingestion.client.requests.get",
        return_value=response,
    ) as mock_get:

        result = client.get("/cars")

    assert result == {
        "data": []
    }

    mock_get.assert_called_once_with(
        f"{client.base_url}/cars",
        params=None,
        timeout=30,
    )


def test_get_passes_params():

    client = VT3APIClient()

    response = type(
        "Response",
        (),
        {
            "status_code": 200,
            "raise_for_status": lambda self: None,
            "json": lambda self: {
                "data": []
            },
        },
    )()

    params = {
        "page": 1,
        "limit": 10,
    }

    with patch(
        "src.ingestion.client.requests.get",
        return_value=response,
    ) as mock_get:

        client.get(
            "/cars",
            params=params,
        )

    mock_get.assert_called_once_with(
        f"{client.base_url}/cars",
        params=params,
        timeout=30,
    )


def test_get_handles_timeout():

    client = VT3APIClient()

    with patch(
        "src.ingestion.client.requests.get",
        side_effect=requests.exceptions.Timeout(),
    ), patch(
        "src.ingestion.client.time.sleep"
    ), patch(
        "src.ingestion.client.logger.exception"
    ) as mock_logger:

        with pytest.raises(
            requests.exceptions.Timeout
        ):
            client.get("/cars")

    mock_logger.assert_called_once()


def test_get_handles_connection_error():

    client = VT3APIClient()

    with patch(
        "src.ingestion.client.requests.get",
        side_effect=requests.exceptions.ConnectionError(),
    ), patch(
        "src.ingestion.client.time.sleep"
    ), patch(
        "src.ingestion.client.logger.exception"
    ) as mock_logger:

        with pytest.raises(
            requests.exceptions.ConnectionError
        ):
            client.get("/cars")

    mock_logger.assert_called_once()


def test_get_handles_http_error():

    client = VT3APIClient()

    response = type(
        "Response",
        (),
        {
            "status_code": 404,
            "raise_for_status": lambda self: (
                (_ for _ in ()).throw(
                    requests.exceptions.HTTPError(
                        "404 Not Found"
                    )
                )
            ),
        },
    )()

    with patch(
        "src.ingestion.client.requests.get",
        return_value=response,
    ), patch(
        "src.ingestion.client.logger.exception"
    ) as mock_logger:

        with pytest.raises(
            requests.exceptions.HTTPError
        ):
            client.get("/cars")

    mock_logger.assert_called_once()


def test_get_handles_generic_request_exception():

    client = VT3APIClient()

    with patch(
        "src.ingestion.client.requests.get",
        side_effect=requests.exceptions.RequestException(),
    ), patch(
        "src.ingestion.client.logger.exception"
    ) as mock_logger:

        with pytest.raises(
            requests.exceptions.RequestException
        ):
            client.get("/cars")

    mock_logger.assert_called_once()


def test_get_retries_after_timeout():

    client = VT3APIClient()

    response = type(
        "Response",
        (),
        {
            "status_code": 200,
            "raise_for_status": lambda self: None,
            "json": lambda self: {
                "data": []
            },
        },
    )()

    with patch(
        "src.ingestion.client.requests.get",
        side_effect=[
            requests.exceptions.Timeout(),
            response,
        ],
    ) as mock_get, patch(
        "src.ingestion.client.time.sleep"
    ) as mock_sleep:

        result = client.get("/cars")

    assert result == {
        "data": []
    }

    assert mock_get.call_count == 2

    mock_sleep.assert_called_once_with(
        1.0
    )


def test_get_retries_after_connection_error():

    client = VT3APIClient()

    response = type(
        "Response",
        (),
        {
            "status_code": 200,
            "raise_for_status": lambda self: None,
            "json": lambda self: {
                "data": []
            },
        },
    )()

    with patch(
        "src.ingestion.client.requests.get",
        side_effect=[
            requests.exceptions.ConnectionError(),
            requests.exceptions.ConnectionError(),
            response,
        ],
    ) as mock_get, patch(
        "src.ingestion.client.time.sleep"
    ) as mock_sleep:

        result = client.get("/cars")

    assert result == {
        "data": []
    }

    assert mock_get.call_count == 3

    assert mock_sleep.call_count == 2

    assert mock_sleep.call_args_list == [
        ((1.0,), {}),
        ((1.0,), {}),
    ]


def test_get_retries_after_retryable_http_error():

    client = VT3APIClient()

    response_503 = type(
        "Response",
        (),
        {
            "status_code": 503,
            "raise_for_status": lambda self: (
                (_ for _ in ()).throw(
                    requests.exceptions.HTTPError(
                        "503 Service Unavailable"
                    )
                )
            ),
        },
    )()

    response_success = type(
        "Response",
        (),
        {
            "status_code": 200,
            "raise_for_status": lambda self: None,
            "json": lambda self: {
                "data": []
            },
        },
    )()

    with patch(
        "src.ingestion.client.requests.get",
        side_effect=[
            response_503,
            response_success,
        ],
    ) as mock_get, patch(
        "src.ingestion.client.time.sleep"
    ) as mock_sleep:

        result = client.get("/cars")

    assert result == {
        "data": []
    }

    assert mock_get.call_count == 2

    mock_sleep.assert_called_once_with(
        1.0
    )


def test_get_does_not_retry_non_retryable_http_error():

    client = VT3APIClient()

    response = type(
        "Response",
        (),
        {
            "status_code": 404,
            "raise_for_status": lambda self: (
                (_ for _ in ()).throw(
                    requests.exceptions.HTTPError(
                        "404 Not Found"
                    )
                )
            ),
        },
    )()

    with patch(
        "src.ingestion.client.requests.get",
        return_value=response,
    ) as mock_get, patch(
        "src.ingestion.client.time.sleep"
    ) as mock_sleep:

        with pytest.raises(
            requests.exceptions.HTTPError
        ):
            client.get("/cars")

    assert mock_get.call_count == 1

    mock_sleep.assert_not_called()


def test_get_stops_after_max_retries():

    client = VT3APIClient()

    with patch(
        "src.ingestion.client.requests.get",
        side_effect=requests.exceptions.Timeout(),
    ) as mock_get, patch(
        "src.ingestion.client.time.sleep"
    ) as mock_sleep:

        with pytest.raises(
            requests.exceptions.Timeout
        ):
            client.get("/cars")

    assert mock_get.call_count == 4

    assert mock_sleep.call_count == 3