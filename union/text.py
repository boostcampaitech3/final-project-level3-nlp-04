import sys
import json
sys.path.append("../")
from extraction.serialization import get_serialization_string

"""
model에 들어 가기 전 email, phone 추출 및 preprocessing Module
"""

def preprocess_for_tagging(ocr_output: json):
    info_dict = get_serialization_string(ocr_output)

    email = info_dict["email"]
    phone = info_dict["phone"]

    del info_dict["email"]
    del info_dict["phone"]
    info_dict = " ".join(info_dict.values())

    return email, phone, info_dict