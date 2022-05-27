from util.post_processing import *
from util.preprocess_image import *
from util.logger import *
from util.ocr_api import *


def main():
    logger = get_logger()
    config = load_config()

    with timer("api", logger):
        res = call_ocr_api(config=config)

    #########################################################
    with timer("preprocessing", logger):
        ## image preprocessing (1 ~ 4)
        # 1. call_ocr_api : ocr ,api를 통해 Raw image의 글자 위치 정보 등을 불러온다.
        pre_ocr_output = call_ocr_api(config=config)

        # 2. find_degree_and_point : ocr output을 기반으로 이미지의 회전각과 명함의 중점을 파악한다.
        img_degree, mid_point_x, mid_point_y = find_degree_and_point(pre_ocr_output)

        # 3. rotate_image : 파악한 정보를 통해 이미지를 알맞게 회전시킨다.
        rotate_img = rotate_image(str(config["ocr"]["path"]), img_degree, mid_point_x, mid_point_y)

        # 4. crop_image : 이미지에서 명함만 인식하여 crop한다.
        preprocessed_img = crop_image(rotate_img)

        # 5. type to binary : bytes 형태로 변환
        bin_img = img_to_binary(preprocessed_img)
    ##########################################################

    with timer("after preprocessing api", logger):
        res = call_ocr_api(config=config, custom_path=bin_img)
    res = sectorization(res)
    email, phone, company = get_valid_info(res)
    # res = post_processing_2(res)
    
    """
    TODO : tagging

    """
    print(f"EMAIL : {email}")
    print(f"PHONE : {phone}")
    print(f"COMPANY : {company}")

    return res

if __name__=="__main__":
    main()