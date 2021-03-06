# ๐ช Upstage Post OCR Parsing Project (๋ชํจ ์ ๋ณด ์ถ์ถ)

## Introduction

### ๐คช Team ์ ์พํ ๋ฐ๋ 



#### ๐ Members  

๊น์ค์|์์ธ๋ฒ|์ก์์ค|์ฌํจ์|์ ์ํ|
:-:|:-:|:-:|:-:|:-:
<img src='https://avatars.githubusercontent.com/u/71753257?v=4' height=80 width=80px></img>|<img src='https://avatars.githubusercontent.com/u/92137358?v=4' height=80 width=80px></img>|<img src='https://avatars.githubusercontent.com/u/55626702?v=4' height=80 width=80px></img>|<img src='https://avatars.githubusercontent.com/u/62679143?v=4' height=80 width=80px></img>|<img src='https://user-images.githubusercontent.com/46811558/157460704-6a5ac09f-fe71-4dd3-b30a-f2fa347b08d2.jpg' height=80 width=80px></img>
[Github](https://github.com/junseok0408)|[Github](https://github.com/inbeomi)|[Github](https://github.com/addadda15)|[Github](https://github.com/hyoeun98)|[Github](https://github.com/jungsiroo)
 
#### ๐ Contribution  

- [`๊น์ค์`](https://github.com/junseok0408) &nbsp; Image Preprocess, Serialization, Multi-threading, Text Post Process
- [`์์ธ๋ฒ`](https://github.com/inbeomi) &nbsp; Model Research, Metric, Data Annotation
- [`์ก์์ค`](https://github.com/addadda15) &nbsp; Serialization, Fast API Server, Android App Develop
- [`์ฌํจ์`](https://github.com/hyoeun98) &nbsp; Multi-threading, Modularity, Construct Pipeline, Refactoring
- [`์ ์ํ`](https://github.com/jungsiroo) &nbsp; Serialization, Text PreยทPost Process, Android App Develop, Refactoring


## Project Outline

### ๐ฏ ํ๋ก์ ํธ ๋ชฉํ 

* ๋ชฉ์ 
    * ๋ชํจ์ ์ ๋ณด(์ด๋ฆ, ์ง์ฑ, ์ฃผ์, ํ์ฌ๋ช, ์ ํ๋ฒํธ, ์ด๋ฉ์ผ) ์ถ์ถ
    * ์ถ์ถ๋ ์ ๋ณด๋ฅผ ์ฑ์ ํ๋ฉด์ผ๋ก ์ถ๋ ฅ
* ์ฃผ์ ๊ธฐ๋ฅ
    * ๋ชํจ ์ด๋ฏธ์ง ์นด๋ฉ๋ผ๋ก ์ฐ๊ฑฐ๋ ๊ฐค๋ฌ๋ฆฌ์์ ์ ํ ๊ฐ๋ฅ
    * ์ด๋ฏธ์ง๋ฅผ ์ ๋ฐฉํฅ์ผ๋ก ์ ์ฒ๋ฆฌ
    * ์ ์ฒ๋ฆฌ๋ ์ด๋ฏธ์ง์์ ์ํ๋ ์ ๋ณด๋ฅผ ์ถ์ถ

### ๐ญ ํ๋ก์ ํธ ์ ์ฒด ๊ตฌ์กฐ

![project_figure](https://user-images.githubusercontent.com/55626702/172746664-b37a2427-f770-4fcc-b8e5-0f93bc5d47a2.PNG)

## Demo

### ๐ ๋ชํจ ์ธ์ ์ฑ ๊ตฌ๋ ์์ 


![ezgif-4-e56ff915ab](https://user-images.githubusercontent.com/54366260/172990038-4fafa836-0f55-4d15-87d7-feb230b7a3a6.gif)





## ๐ Architecture
```
.
โโโ app.py
โโโ main.py
โโโ model
โ โโโ dataloader.py
โ โโโ dataset.py
โ โโโ inference.py
โ โโโ tag2id.pkl
โ โโโ train.py
โ โโโ utilities.py
โโโ calculate
โ โโโ metric.py
โ โโโ pickle.py
โโโ extraction
โ โโโ detection.py
โ โโโ serialization.py
โ โโโ valid_info.py
โโโ preprocess
โ โโโ cleansing.py
โ โโโ image.py
โโโ union
โ โโโ image.py
โ โโโ text.py
โโโ util
โ โโโ log_and_config.py
โ โโโ ocr_api.py
โ โโโ translation.py
โโโ yaml
โ โโโ config.yaml
โ โโโ log_config.yaml
โโโ log
โ โโโ info.log
โโโ README.md
โโโ requirements.txt
```

## ๐จ How to Use

```bash
# ํ๋ก์ ํธ ๋ค์ด๋ก๋
git clone https://github.com/boostcampaitech2/final-project-level3-nlp-14.git
cd final-project-level3-nlp-14

pip install -r requirements.txt

python app.py
```

Metric ์คํ
```bash
python app.py --calculate True >> metric_result
```

## ๐ฌDocker
```
docker pull a2921641/post_ocr:latest
docker run a2921641/post_ocr -p 30001:30001
```
