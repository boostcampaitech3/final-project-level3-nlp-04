import requests
import json
import os
import glob

api_url = "http://118.222.179.32:30001/ocr/"
headers = {"secret": "Boostcamp0001"}
dir_name = '/opt/ml/input/code/OCR/sample/*.jpg' # 데이터가 있는 폴더랑 확장자 수정

for file_name in glob.glob(dir_name):

    file_dict = {"file": open(file_name, "rb")}
    response = requests.post(api_url, headers=headers, files=file_dict)
    data = response.json()
    
    file_name = file_name.split('/')[-1][:-4] # 확장자가 jpg나 png같이 3글자이면 -4
    output_path = f'./output'
    if not os.path.isdir(output_path):
        os.mkdir(output_path)
    output_path = f'./output/{file_name}.json' #output 폴더에 저장

    with open(output_path, 'w',encoding='utf-8') as f:
        json.dump(data, f,ensure_ascii=False,indent=4)

