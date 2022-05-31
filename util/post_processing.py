import json
import sys
from typing import DefaultDict, Tuple 
sys.path.append("util")
from make_context import *

def sectorization(response: json):  # dict?
    info_dict = get_serialization_string(response)

    email, phone = get_valid_info(info_dict)
    info_dict = get_raw_dict_info(info_dict)

    return email, phone, info_dict


def get_valid_info(response : DefaultDict)->Tuple[str, str]:  # 필요하면 추가
    email = response["email"]
    phone = response["phone"]

    return email, phone

def get_raw_dict_info(response):  # 필요하면 추가
    del response["email"]
    del response["phone"]

    return response
