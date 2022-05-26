from typing import Dict
from yaml import load, FullLoader
import logging
import logging.config


def load_log_config(config_path: str = "log_config.yaml") -> Dict[str, any]:
    with open(config_path, "r") as f:
        config = load(f, FullLoader)
    return config


def get_logger():
    logger_config = load_log_config("./log/log_config.yaml")
    logging.config.dictConfig(logger_config)
    logger = logging.getLogger("api_logger")
    return logger
