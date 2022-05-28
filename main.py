from util.main import *

def main(img_byte:str):
    logger = get_logger()

    with timer("api", logger):
        res = call_ocr_api(img_byte=img_byte)

    # with timer("preprocessing", logger):
    bin_img = preprocessing_image(img_byte, res)

    # with timer("after preprocessing api", logger):
    res = call_ocr_api(bin_img)

    return post_processing(res)

    """
    TODO : tagging

    """


