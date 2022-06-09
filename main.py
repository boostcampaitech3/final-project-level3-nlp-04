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

    pre_res = call_ocr_api(img)
    bin_imgs = preprocessing_image(img, pre_res)

    pre_imgs = img_augmentation(bin_imgs)

    ocr_result = multi_threading_call_ocr_api(pre_imgs)

    features = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=len(ocr_result)) as exe:
        future_to_api = {
            exe.submit(img_to_features, img, model, tokenizer, device, finder): img
            for img in ocr_result
        }
    for future in concurrent.futures.as_completed(future_to_api):
        features.append(future.result())

    return ensemble(features)
