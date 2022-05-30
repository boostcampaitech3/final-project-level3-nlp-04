from util.main import *

def main(img_byte:str, model, tokenizer, device):
    logger = get_logger()

    with timer("api", logger):
        res = call_ocr_api(img_byte=img_byte)

    # with timer("preprocessing", logger):
        bin_img = preprocessing_image(img_byte, res)

        # with timer("after preprocessing api", logger):
        res = call_ocr_api(bin_img)

        email_phone, dict_info = post_processing(res)

        return inf_main(dict_info, model, tokenizer, device)
