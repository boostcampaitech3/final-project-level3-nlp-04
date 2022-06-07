import json
from pathlib import PosixPath
from pydantic import BaseModel, FilePath, validator, HttpUrl
from typing import Union, Dict, List
import requests
import numpy as np
import concurrent.futures
import sys
sys.path.append("../")
from preprocess.image import img_to_binary
from util.log_and_config import *


class ImagePath(BaseModel):
    path: Union[FilePath, HttpUrl, bytes]

    @validator("path")
    def is_path(cls, v):
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

        elif isinstance(v, bytes):
            return v

        else:
            raise ValueError("Invalid path type")


def get_img_path(path: str) -> ImagePath:
    return ImagePath(path=path)


def call_ocr_api(img: Union[bytes, ImagePath]) -> json:
    img_path = get_img_path(img)
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
            file_dict = {"file": img_path.path}
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
