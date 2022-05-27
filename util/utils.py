from typing import List
import sys
sys.path.append("./utils")
from ocr_api import *
from make_context import *

def get_string_list(img_path:str, on_local=True)->List:
    api_output = upload_local_file(img_path=img_path) if on_local else upload_web_file(img_path=img_path)
    return get_serialization_string(api_output=api_output)
