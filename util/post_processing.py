import json
import sys
from typing import DefaultDict, Tuple 
sys.path.append("util")
from make_context import *


def sectorization(response: json):  # dict?
    return get_serialization_string(response)


def get_valid_info(response : DefaultDict)->Tuple[str, str]:  # 필요하면 추가
    email = response["email"]
    phone = response["phone"]

    return email, phone

def get_dict_info(response):  # 필요하면 추가
    del response["email"]
    del response["phone"]

    return response
