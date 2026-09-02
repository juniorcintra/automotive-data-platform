import logging

from src.core.logger import (
    get_logger,
)


def test_get_logger_returns_logger():

    logger = get_logger(
        "test_logger"
    )

    assert isinstance(
        logger,
        logging.Logger,
    )


def test_get_logger_sets_info_level():

    logger = get_logger(
        "test_logger_level"
    )

    assert logger.level == logging.INFO


def test_get_logger_does_not_duplicate_handlers():

    logger = get_logger(
        "test_logger_handlers"
    )

    initial_handlers_count = len(
        logger.handlers
    )

    get_logger(
        "test_logger_handlers"
    )

    assert len(
        logger.handlers
    ) == initial_handlers_count