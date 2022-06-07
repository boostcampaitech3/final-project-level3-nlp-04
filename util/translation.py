from util.log_and_config import load_config
import requests


def get_translate(text, lan1, lan2, num):
    config = load_config()
    client_id_list = config["naver_api"]["id"]
    client_secret_list = config["naver_api"]["pw"]

    data = {"text": text, "source": lan1, "target": lan2}

    url = config["naver_api"]["url"]

    header = {
        "X-Naver-Client-Id": client_id_list[num],
        "X-Naver-Client-Secret": client_secret_list[num],
    }

    response = requests.post(url, headers=header, data=data)
    rescode = response.status_code

    if rescode == 200:
        t_data = response.json()
        return t_data["message"]["result"]["translatedText"]
    else:
        return rescode
