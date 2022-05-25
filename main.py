from utils import *
from post_processing import *
from pre_processing import *

config = load_config()
path = config["ocr"]["path"]
path = get_img_path(path)
img = pre_ocr(path)
res = OCR_api(img)

# res = sectorization(res)
# res = post_processing_1(res)
# res = post_processing_2(res)
print(res)

"""
TODO : tagging

"""
