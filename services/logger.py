import logging
import os

LOG_DIR = "logs"
LOG_FILE = os.path.join(LOG_DIR, "smartqueue.log")

_logger: logging.Logger | None = None


def configurar_logger(
    log_file: str | None = None,
) -> logging.Logger:

    global _logger

    caminho = log_file or LOG_FILE

    os.makedirs(
        os.path.dirname(caminho),
        exist_ok=True,
    )

    logger = logging.getLogger("smartqueue")
    logger.setLevel(logging.INFO)
    logger.propagate = False
    logger.handlers.clear()

    handler = logging.FileHandler(
        caminho,
        encoding="utf-8",
    )

    handler.setFormatter(
        logging.Formatter(
            "%(asctime)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
    )

    logger.addHandler(handler)
    _logger = logger

    return logger


def get_logger() -> logging.Logger:

    if _logger is None:
        return configurar_logger()

    return _logger
