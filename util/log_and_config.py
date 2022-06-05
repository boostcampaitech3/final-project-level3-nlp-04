from typing import Dict
from yaml import load, FullLoader
import logging
import logging.config
from contextlib import contextmanager
import time

"""
Logging 및 config 관련 Module
"""


@contextmanager
def timer(name: str, logger: logging.Logger):
    t0 = time.time()
    yield
    logger.info(f"{name} done in {time.time() - t0:.3f} s")


def load_config(config_path: str = "yaml/config.yaml",) -> Dict[str, any]:
    with open(config_path, "r") as f:
        config = load(f, FullLoader)

    return config


def load_log_config(config_path: str = "yaml/log_config.yaml",) -> Dict[str, any]:
    with open(config_path, "r") as f:
        config = load(f, FullLoader)

    return config


def get_logger(logger_name: str = "api_logger") -> logging.Logger:
    logger_config = load_log_config()
    logging.config.dictConfig(logger_config)
    logger = logging.getLogger(logger_name)
    return logger
