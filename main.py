from utils import *
from post_processing import *
from pre_processing import *

# config = load_config()
# path = config["ocr"]["path"]
# path = get_img_path(path)

#########################################################
## image preprocessing (1 ~ 4)
# 1. OCR_api : ocr api를 통해 Raw image의 글자 위치 정보 등을 불러온다.
pre_ocr_output = OCR_api(path)

# 2. find_degree_and_point : ocr output을 기반으로 이미지의 회전각과 명함의 중점을 파악한다.
img_degree, mid_point_x, mid_point_y = find_degree_and_point(pre_ocr_output)

# 3. rotate_image : 파악한 정보를 통해 이미지를 알맞게 회전시킨다.
rotate_img = rotate_image(file_path, img_degree, mid_point_x, mid_point_y)

# 4. crop_image : 이미지에서 명함만 인식하여 crop한다.
preprocessed_img = crop_image(img)


##########################################################

# res = OCR_api(img)
# res = sectorization(res)
# res = post_processing_1(res)
# res = post_processing_2(res)
# print(res)

"""
TODO : tagging

"""
