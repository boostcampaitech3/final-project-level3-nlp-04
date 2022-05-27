from email import header
import json
from pathlib import PosixPath
from pydantic import BaseModel, FilePath, validator, HttpUrl
from typing import Union, Dict
import requests
from yaml import load, FullLoader
from contextlib import contextmanager
import time
import logging


@contextmanager
def timer(name: str, logger: logging.Logger):
    t0 = time.time()
    yield
    logger.info(f"{name} done in {time.time() - t0:.3f} s")


class ImagePath(BaseModel):
    path: Union[FilePath, HttpUrl]

    @validator("path")
    def is_image(cls, v):
        _valid_extension = (".jpg", ".png", ".jpeg")
        if isinstance(v, PosixPath):
            extension = v.suffix
            if extension not in _valid_extension:
                raise ValueError("File is not jpg, png, or jpeg")
            return v

        elif isinstance(v, HttpUrl):
            if not v.endswith(_valid_extension):
                raise ValueError("Url is not jpg, png, or jpeg")
            return v

        else:
            raise ValueError("Invalid path type")


def load_config(
    config_path: str = "/opt/ml/final-project-level3-nlp-04/yaml/config.yaml",
) -> Dict[str, any]:
    with open(config_path, "r") as f:
        config = load(f, FullLoader)

    print(f"Image load from {config['ocr']['path']}")
    return config


def get_img_path(path: str) -> ImagePath:
    return ImagePath(path=path)


def call_ocr_api(config: Dict[str, any], custom_path: bytes = None) -> json:
    img_path = get_img_path(config["ocr"]["path"])
    if custom_path:
        img_path = custom_path

    api_url = config["ocr"]["api_url"]
    headers = config["ocr"]["headers"]

    if isinstance(img_path, ImagePath):
        if isinstance(img_path.path, PosixPath):  # FilePath
            file_dict = {"file": open(img_path.path, "rb")}
            response = requests.post(api_url, headers=headers, files=file_dict)

        elif isinstance(img_path.path, HttpUrl):  # Url
            data = {"url": img_path.path}
            response = requests.post(api_url, headers=headers, data=data)

    else:  # Bytes
        file_dict = {"file": img_path}
        response = requests.post(api_url, headers=headers, files=file_dict)

    return response.json()
