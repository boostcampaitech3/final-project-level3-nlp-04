from matplotlib import collections
from util.log_and_config import *
from util.ocr_api import *
from model.inference import *
from union.image import *
from union.text import *
from extraction.valid_info import *
import concurrent.futures

def img_to_features(imgs, model, tokenizer, device, finder) -> List[OrderedDict]:
    email, phone, info_dict = preprocess_for_tagging(imgs)  # tagging 전처리

    texts, tags = inference(info_dict, model, tokenizer, device, finder)
    output = extract_info(texts, tags, finder)

    output["email"] = email
    output["phone"] = phone

    return get_final_output(output)

def main(img: str, model: str, tokenizer: str, device: str, finder) -> json:

    logger = get_logger()

    with timer("api", logger):
        with timer("preprocessing", logger):
            pre_res = call_ocr_api(img)
            bin_imgs = preprocessing_image(img, pre_res)

        with timer("augmentation", logger):
            pre_imgs = img_augmentation(bin_imgs)

        with timer("multi_ocr", logger):
            ocr_result = multi_threading_call_ocr_api(pre_imgs)

        with timer("output", logger):
            features = []
            with concurrent.futures.ThreadPoolExecutor(
                max_workers=len(ocr_result)
            ) as exe:
                future_to_api = {
                    exe.submit(
                        img_to_features, img, model, tokenizer, device, finder
                    ): img
                    for img in ocr_result
                }
                for future in concurrent.futures.as_completed(future_to_api):
                    features.append(future.result())

        output = OrderedDict(
            {"이름": "", "직책": "", "회사명": "", "주소": "", "전화번호": "", "이메일": ""}
        )
        for i in features:
            output["이름"] += i["이름"]
            output["직책"] += i["직책"]
            output["회사명"] += i["회사명"]
            output["주소"] += i["주소"]
            output["전화번호"] += i["전화번호"]
            output["이메일"] += i["이메일"]

        return ensemble(features)
