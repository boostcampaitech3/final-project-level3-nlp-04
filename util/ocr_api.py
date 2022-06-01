import json
from pathlib import PosixPath
from pydantic import BaseModel, FilePath, Json, validator, HttpUrl
from typing import Union, Dict, List
import requests
from yaml import load, FullLoader
from contextlib import contextmanager
import time
import logging
import numpy as np
import concurrent.futures
import cv2
from preprocess_image import img_to_binary


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


def load_config(config_path: str = "./yaml/config.yaml",) -> Dict[str, any]:
    with open(config_path, "r") as f:
        config = load(f, FullLoader)

    return config


def get_img_path(path: str) -> ImagePath:
    return ImagePath(path=path)


def call_ocr_api(img_byte: bytes) -> json:
    img_path = img_byte
    config = load_config()
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


def multi_threading_call_ocr_api(img_list: List[np.ndarray]) -> List[Dict]:
    bin_list = list(map(img_to_binary, img_list))
    result = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=len(bin_list)) as exe:
        future_to_api = {exe.submit(call_ocr_api, file): file for file in bin_list}
        for future in concurrent.futures.as_completed(future_to_api):
            result.append(future.result())

    return result
