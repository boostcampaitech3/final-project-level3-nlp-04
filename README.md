# 🟪 Upstage Post OCR Parsing Project (명함 정보 추출)

## 1. Introduction

### Team 유쾌한 반란



#### 🔅 Members  

김준석|서인범|송영준|심효은|정시현|
:-:|:-:|:-:|:-:|:-:
<img src='https://avatars.githubusercontent.com/u/71753257?v=4' height=80 width=80px></img>|<img src='https://avatars.githubusercontent.com/u/92137358?v=4' height=80 width=80px></img>|<img src='https://avatars.githubusercontent.com/u/55626702?v=4' height=80 width=80px></img>|<img src='https://avatars.githubusercontent.com/u/62679143?v=4' height=80 width=80px></img>|<img src='https://user-images.githubusercontent.com/46811558/157460704-6a5ac09f-fe71-4dd3-b30a-f2fa347b08d2.jpg' height=80 width=80px></img>
[Github](https://github.com/junseok0408)|[Github](https://github.com/inbeomi)|[Github](https://github.com/addadda15)|[Github](https://github.com/hyoeun98)|[Github](https://github.com/jungsiroo)
junseok0408@konkuk.ac.kr|inbeom0907@gmail.com|songjun5711@gmail.com|f2921641@naver.com|sh2298@naver.com
 
#### 🔅 Contribution  

- [`김준석`](https://github.com/junseok0408) &nbsp; Image Preprocess, Serialization, Multi-threading, Text Post Process
- [`서인범`](https://github.com/inbeomi) &nbsp; Model Research, Metric, Data Annotation
- [`송영준`](https://github.com/addadda15) &nbsp; Serialization, Fast API Server, Android App Develop
- [`심효은`](https://github.com/hyoeun98) &nbsp; Multi-threading, Modularity, Construct Pipeline, Refactoring
- [`정시현`](https://github.com/jungsiroo) &nbsp; Serialization, Text Pre·Post Process, Android App Develop, Refactoring


## 2. Project Outline

### 프로젝트 목표

* 목적
    * 명함의 정보(이름, 직책, 주소, 회사명, 전화번호, 이메일) 추출
    * 추출된 정보를 앱의 화면으로 출력
* 주요 기능
    * 명함 이미지 카메라로 찍거나 갤러리에서 선택 가능
    * 이미지를 정방향으로 전처리
    * 전처리된 이미지에서 원하는 정보를 추출

### 프로젝트 전체 구조

![project_figure](https://user-images.githubusercontent.com/55626702/172746664-b37a2427-f770-4fcc-b8e5-0f93bc5d47a2.PNG)

## 3. Demo

### 👀 명함 인식 앱 구동 예시

## 4. How to Use
```
.
├── app.py
├── main.py
├── model
│ ├── dataloader.py
│ ├── dataset.py
│ ├── inference.py
│ ├── tag2id.pkl
│ ├── train.py
│ └── utilities.py
├── calculate
│ ├── metric.py
│ └── pickle.py
├── extraction
│ ├── detection.py
│ ├── serialization.py
│ └── valid_info.py
├── preprocess
│ ├── cleansing.py
│ ├── image.py
├── union
│ ├── image.py
│ └── text.py
├── util
│ ├── log_and_config.py
│ ├── ocr_api.py
│ └── translation.py
└── yaml
│ ├── config.yaml
│ └── log_config.yaml
├── log
│ └── info.log
├── README.md
├── requirements.txt
```

## Docker
```
docker pull a2921641/post_ocr:latest
docker run a2921641/post_ocr:latest -p 30001:30001
```

아래 명령어로 실행 가능합니다.

```bash
# 프로젝트 다운로드
git clone https://github.com/boostcampaitech2/final-project-level3-nlp-14.git --recursive
cd final-project-level3-nlp-14
git submodule update --recursive
# 프론트엔드 환경설정
cd frontend
npm install
npm run build
cd ..
# 백엔드 환경설정
poetry shell
poetry install
poe force-cuda11
poe init-vqa
python app.py
```
