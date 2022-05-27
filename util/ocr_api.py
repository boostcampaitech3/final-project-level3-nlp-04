import requests
import json

## 사용시 주의사항
# 반드시 서버 별 올바른 header 값을 넘겨주셔야 합니다.
# 파일 입력은 *.jpg, *.png, *.jpeg 형태만 입력 가능합니다.
# payload는 반드시 file 또는 url 필드 1개만 전달되어야 합니다.

## Server 1
api_url = "http://118.222.179.32:30000/ocr/"
headers = {"secret": "Boostcamp0000"}

## Server 2
# api_url = "http://118.222.179.32:30001/ocr/"
# headers = {"secret": "Boostcamp0001"}

## 방법 1. 파일 업로드
def upload_local_file(img_path)->json:
    file_dict = {"file": open(img_path, "rb")}
    response = requests.post(api_url, headers=headers, files=file_dict)
    # pprint.pprint(response.json())

    return response.json()

## 방법 2. 파일 URL 전달
def upload_web_file(img_path)->json:
    data = {
        "url": img_path 
    }
    response = requests.post(api_url, headers=headers, data=data)
    # pprint.pprint(response.json())

    return response.json()
