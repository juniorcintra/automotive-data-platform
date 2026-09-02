import logging

from src.core.config import LOG_LEVEL


def get_logger(
    name: str,
) -> logging.Logger:
    """
    Cria e configura um logger
    para a aplicação.
    """

    logger = logging.getLogger(name)

    log_level = getattr(
        logging,
        LOG_LEVEL.upper(),
        logging.INFO,
    )

    logger.setLevel(
        log_level
    )

    if not logger.handlers:

        handler = logging.StreamHandler()

        handler.setLevel(
            log_level
        )

        formatter = logging.Formatter(
            "%(asctime)s | "
            "%(levelname)s | "
            "%(name)s | "
            "%(message)s"
        )

        handler.setFormatter(
            formatter
        )

        logger.addHandler(
            handler
        )

    return logger