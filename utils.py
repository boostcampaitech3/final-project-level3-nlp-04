import json
from pathlib import PosixPath
from pydantic import BaseModel, FilePath, validator, HttpUrl
from typing import Union, Dict
import requests
from yaml import load, FullLoader


class ImagePath(BaseModel):
    path: Union[FilePath, HttpUrl]

    @validator("path")
    def is_image(cls, v):
        _valud_extension = (".jpg", ".png", ".jpeg")
        if isinstance(v, PosixPath):
            extension = v.suffix
            if extension not in _valud_extension:
                raise ValueError("File is not jpg, png, or jpeg")
            return v

        elif isinstance(v, HttpUrl):
            if not v.endswith(_valud_extension):
                raise ValueError("Url is not jpg, png, or jpeg")
            return v

        else:
            raise ValueError("Invalid path type")


def load_config(config_path: str = "config.yaml") -> Dict[str, any]:
    with open(config_path, "r") as f:
        config = load(f, FullLoader)
    return config


def get_img_path(path: str) -> ImagePath:
    return ImagePath(path=path)


def OCR_api(img_path: Union[ImagePath, bytes]) -> json:
    config = load_config()
    api_url = config["ocr"]["api_url"]
    headers = config["ocr"]["headers"]
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


# path = "/opt/ml/img/raw_image_5.jpg"
# path = "https://upload.wikimedia.org/wikipedia/commons/7/78/Tesseract_OCR_logo_%28Google%29.png"
# path = get_img_path(path)
# print(path)
# response = OCR_api(path)
# print(response)

