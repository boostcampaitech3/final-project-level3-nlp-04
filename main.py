from util.main import *

def main(img_byte:str, model, tokenizer, device, finder):
    logger = get_logger()

    with timer("api", logger):
        res = call_ocr_api(img_byte=img_byte)

        bin_img = preprocessing_image(img_byte, res)
        res = call_ocr_api(bin_img)
        email, phone, info_dict = preprocess_for_tagging(res)

        output = inf_main(info_dict, model, tokenizer, device, finder)

        output["email"] = email
        output["phone"] = phone

        return output

