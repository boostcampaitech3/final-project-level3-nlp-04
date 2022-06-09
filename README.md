# 🟪 Upstage Post OCR Parsing Project (명함 정보 추출) 🟪

## 1. Introduction

### Team 유쾌한 반란



#### 🔅 Members  

김준석|서인범|심효은|정시현|송영준|
:-:|:-:|:-:|:-:|:-:
<img src='https://avatars.githubusercontent.com/u/71753257?v=4' height=80 width=80px></img>|<img src='https://avatars.githubusercontent.com/u/92137358?v=4' height=80 width=80px></img>|<img src='https://user-images.githubusercontent.com/46811558/157460704-6a5ac09f-fe71-4dd3-b30a-f2fa347b08d2.jpg' height=80 width=80px></img>
[Github](https://github.com/junseok0408)|[Github](https://github.com/inbeomi)|[Github](https://github.com/hyoeun98)|[Github](https://github.com/jungsiroo)|[Github](https://github.com/addadda15)|<img src='https://avatars.githubusercontent.com/u/55626702?v=4' height=80 width=80px></img>|<img src='https://avatars.githubusercontent.com/u/62679143?v=4' height=80 width=80px></img>|
 
#### 🔅 Contribution  

- [`김준석`](https://github.com/junseok0408) &nbsp; Image Preprocess, Serialization, Multi-threading, Text Post Process
- [`서인범`](https://github.com/inbeomi) &nbsp; Model Research, Metric, Data Annotation
- [`심효은`](https://github.com/hyoeun98) &nbsp; Multi-threading, Modularity, Construct Pipeline, Refactoring
- [`정시현`](https://github.com/jungsiroo) &nbsp; Serialization, Text Pre·Post Process, Android App Develop, Refactoring
- [`송영준`](https://github.com/addadda15) &nbsp; Serialization, Fast API Server, Android App Develop


## 2. Project Outline

### 프로젝트 목표

* 목적
    * 명함의 정보(이름, 직책, 주소, 회사명, 전화번호, 이메일) 추출
    * 추출된 정보를 앱의 화면으로 출력
* 주요 기능
    * 명함 이미지을 카메라로 찍거나 갤러리에서 선택 가능
    * 이미지를 정방향으로 전처리
    * 전처리된 이미지에서 원하는 정보를 추출

### 프로젝트 전체 구조

![project_figure](https://user-images.githubusercontent.com/55626702/172746664-b37a2427-f770-4fcc-b8e5-0f93bc5d47a2.PNG)

## 3. Demo

### 📖 ODQA 예시
![ODQA 예시](https://user-images.githubusercontent.com/35680202/147240932-0f44c8e1-f55c-417f-a9b3-df48e62eb3d0.gif)

### 👀 VQA 예시
![VQA 예시](https://user-images.githubusercontent.com/35680202/147241018-95e33ffe-da80-434c-a65c-41a8cf820b62.gif)

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


## 5. References

### Datasets

- [KorQuAD v2.0](https://korquad.github.io/)
    - 라이센스 : CC BY-ND 2.0 KR
- [KLUE - MRC](https://github.com/KLUE-benchmark/KLUE)
    - 라이센스 : CC BY-SA 4.0
- [KVQA(Korean Visual Question Answering)](https://github.com/SKTBrain/KVQA)
    - 라이센스 : [Korean VQA License](https://github.com/SKTBrain/KVQA/blob/master/LICENSE)
- [AI HUB 개방 데이터](https://aihub.or.kr/aihub-data/natural-language/about)
    - 라이센스 : https://aihub.or.kr/intro/policy


### Paper
- [Antol, Stanislaw, et al. "Vqa: Visual question answering." Proceedings of the IEEE international conference on computer vision. 2015](https://www.cv-foundation.org/openaccess/content_iccv_2015/papers/Antol_VQA_Visual_Question_ICCV_2015_paper.pdf)
- [Yang, Zichao, et al. "Stacked attention networks for image question answering." Proceedings of the IEEE conference on computer vision and pattern recognition. 2016](https://openaccess.thecvf.com/content_cvpr_2016/papers/Yang_Stacked_Attention_Networks_CVPR_2016_paper.pdf)
- [Jin-Hwa Kim, Jaehyun Jun, and Byoung-Tak Zhang. "Bilinear attention networks." Advances in Neural Information Processing Systems 31. 2018](https://papers.nips.cc/paper/2018/file/96ea64f3a1aa2fd00c72faacf0cb8ac9-Paper.pdf)
- [Jin-Hwa Kim, Soohyun Lim, et al. "Korean Localization of Visual Question Answering for Blind People." AI for Social Good workshop at NeurIPS. 2019](https://aiforsocialgood.github.io/neurips2019/accepted/track1/pdfs/44_aisg_neurips2019.pdf)
- [Anderson, Peter, et al. "Bottom-up and top-down attention for image captioning and visual question answering." Proceedings of the IEEE conference on computer vision and pattern recognition. 2018.](https://openaccess.thecvf.com/content_cvpr_2018/CameraReady/1163.pdf)
- [Xu et al., Curriculum Learning for Natural Language Understanding, ACL 2020](https://aclanthology.org/2020.acl-main.542.pdf)
- [ZHANG, Zhuosheng; YANG, Junjie; ZHAO, Hai. Retrospective reader for machine reading comprehension. arXiv preprint arXiv:2001.09694, 2020.](https://arxiv.org/pdf/2001.09694.pdf")

### Software
#### Open-Domain Question Answering - Reader
- [monologg/koelectra-small-v3-discriminator](https://huggingface.co/monologg/koelectra-small-v3-discriminator)
- [huggingface/datasets](https://github.com/huggingface/datasets)
- [huggingface/transformers](https://github.com/huggingface/transformers)
- [retro reader](https://github.com/cooelf/AwesomeMRC)

#### Open-Domain Question Answering - Retrieval
- [elastricsearch](https://github.com/elastic/elasticsearch-py)

#### Visual Question Answering
- [MILVLG/bottom-up-attention](https://github.com/MILVLG/bottom-up-attention.pytorch)
- [Shivanshu-Gupta/Stacked Attention Network](https://github.com/Shivanshu-Gupta/Visual-Question-Answering)
- [SKTBrain/BAN-KVQA](https://github.com/SKTBrain/BAN-KVQA)

#### Web Frameworks
- [Vuejs/Vuetify](https://github.com/vuetifyjs/vuetify)
- [FastAPI](https://github.com/tiangolo/fastapi)
- [Stremlit](https://github.com/streamlit/streamlit)



# final-project-level3-nlp-04

