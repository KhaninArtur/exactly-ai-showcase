import logging


def setup_logging():
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger("uvicorn")

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s"))

    logger.addHandler(console_handler)


def get_logger() -> logging.Logger:
    return logging.getLogger("uvicorn")
