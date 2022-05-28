import sys
sys.path.append("./util")
from logger import *
from ocr_api import *
from post_processing import *
from preprocess_image import *

def preprocessing_image(img_byte, ocr_output):
    img_degree, mid_point_x, mid_point_y = find_degree_and_point(ocr_output)

    # 2. rotate_image : 파악한 정보를 통해 이미지를 알맞게 회전시킨다.
    rotate_img = rotate_image(
        img_byte, img_degree, mid_point_x, mid_point_y
    )

    # 3. crop_image : 이미지에서 명함만 인식하여 crop한다.
    preprocessed_img = crop_image(rotate_img)

    # 4. type to binary : bytes 형태로 변환
    bin_img = img_to_binary(preprocessed_img)

    return bin_img

def post_processing(ocr_output):
    res = sectorization(ocr_output)

    email, phone = get_valid_info(res)

    ret = f"""email : {email}
    phone : {phone}"""

    return ret 