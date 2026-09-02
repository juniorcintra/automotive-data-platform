import logging

from src.core.logger import get_logger


def test_get_logger_returns_logger():

    logger = get_logger(
        "test.logger"
    )

    assert isinstance(
        logger,
        logging.Logger,
    )


def test_get_logger_has_handler():

    logger = get_logger(
        "test.handler"
    )

    assert len(logger.handlers) == 1


def test_get_logger_does_not_duplicate_handlers():

    logger_name = "test.duplicate"

    logger = get_logger(
        logger_name
    )

    get_logger(
        logger_name
    )

    assert len(logger.handlers) == 1


def test_get_logger_uses_info_as_default_level():

    logger = get_logger(
        "test.level"
    )

    assert logger.level == logging.INFO