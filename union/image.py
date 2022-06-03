import sys
sys.path.append("../")
from preprocess.image import *

"""
model에 들어 가기 전 email, phone 추출 및 preprocessing Module
"""

def preprocessing_image(img: bytes, ocr_output: Dict) -> bytes:
    img_degree, mid_point_x, mid_point_y = find_degree_and_point(ocr_output)

    # 2. rotate_image : 파악한 정보를 통해 이미지를 알맞게 회전시킨다.
    rotate_img = rotate_image(img, img_degree, mid_point_x, mid_point_y)

    # 3. crop_image : 이미지에서 명함만 인식하여 crop한다.
    try:
        preprocessed_img = crop_image(rotate_img)
    except:
        preprocessed_img = rotate_image

    # 4. type to binary : bytes 형태로 변환
    bin_img = img_to_binary(preprocessed_img)

    return bin_img
