from tracemalloc import start
from utils import *
from post_processing import *
from pre_processing import *
from logger import *
import time

logger = get_logger()

config = load_config()
path = config["ocr"]["path"]
path = get_img_path(path)
logger.info(f"path={path.path}")
img = pre_ocr(path)

start_time = time.time()
res = OCR_api(img)
end_time = time.time() - start_time
logger.info(f"term={end_time:6f}")

# res = sectorization(res)
# res = post_processing_1(res)
# res = post_processing_2(res)

"""
TODO : tagging

"""
