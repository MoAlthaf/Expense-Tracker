import logging


def setup_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    if not logger.hasHandlers():
        # Console handler
        console = logging.StreamHandler()
        console.setLevel(logging.WARNING)
        logger.addHandler(console)

        # File handler
        file_handler = logging.FileHandler(f"{name}.log")
        file_handler.setLevel(logging.INFO)
        logger.addHandler(file_handler)

        # Formatter
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        console.setFormatter(formatter)
        file_handler.setFormatter(formatter)

    return logger
