import logging
import os
import sys

from EasyWorkEnv import Config


def setup_logging():
    os.makedirs("log", exist_ok=True)
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    console_handler.setFormatter(console_formatter)

    file_handler = logging.FileHandler(
        "log/app.log", mode="a", encoding="utf-8"
    )
    file_handler.setLevel(logging.DEBUG)
    file_formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    file_handler.setFormatter(file_formatter)

    uvicorn_logger = logging.getLogger("uvicorn")
    uvicorn_logger.propagate = False

    uvicorn_access_logger = logging.getLogger("uvicorn.access")
    uvicorn_access_logger.setLevel(logging.INFO)

    fastapi_logger = logging.getLogger("fastapi")
    fastapi_logger.setLevel(logging.INFO)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
