import logging


def create_logger(name: str) -> logging.Logger:
    """
    Create and configure a logger for a project component.
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # Prevent adding another handler if the function is called again
    if not logger.handlers:
        console_handler = logging.StreamHandler()

        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
            datefmt="%H:%M:%S"
        )

        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    return logger