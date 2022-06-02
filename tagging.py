from typing import DefaultDict
import itertools
import re
from text_cleaning import *
from util.translation import *

"""
Detection 함수 Module
"""


def detect_phone(serialized: DefaultDict) -> DefaultDict:
    stack = []
    phone_list = []

    for val in itertools.chain.from_iterable(serialized.values()):
        if val.isdigit():
            if stack:
                stack[-1] += val
            else:
                stack.append(val)

            if not stack[-1].startswith("0"):
                stack.clear()
                continue

            if len(stack[-1]) > 7 and len(stack[-1]) < 12:
                phone_list.append(stack[-1])
                stack.clear()

    serialized = remove_duplicate(serialized, phone_list)
    phone_list = list(filter(lambda x: x.startswith("010"), phone_list))
    serialized["phone"].extend(phone_list)

    return serialized


def detect_email(serialized: DefaultDict) -> DefaultDict:
    stack = []
    email_list = []
    p = re.compile("^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")

    for val in itertools.chain.from_iterable(serialized.values()):
        if p.match(val):
            email_list.append(val)
            break

        stack.append(val)
        val = cleaning_domain(val)

        if "@" in stack[-1]:
            stack.clear()
            stack.append(val)
        elif len(stack) > 1 and "@" in stack[-2]:
            temp = stack[-2]
            stack.clear()
            stack.append(temp + val)

        if p.match(stack[-1]):
            email_list.append(stack[-1])
            break

    serialized = remove_duplicate(serialized, email_list)
    serialized["email"].extend(email_list)

    return serialized


def detect_company(serialized: DefaultDict) -> DefaultDict:
    company_related_sector = [0, 1, 2]
    company_list = []

    for key in company_related_sector:
        for text in serialized[key]:
            text = cleaning_special_token(text)
            company_list.append(text.upper())

    serialized = remove_duplicate(serialized, company_list)
    company = " ".join(company_list)
    serialized["company"].append(company)

    return serialized


def detect_job(sentence, finder):
    # global eng_split_list

    # 기본적인 Rule-Base 병행
    job_list = [
        "매니저",
        "회장",
        "사장",
        "전무",
        "상무",
        "이사",
        "부장",
        "차장",
        "과장",
        "계장",
        "대리",
        "주임",
        "사원",
        "인턴",
        "본부장",
        "지점장",
        "행장",
        "부행장",
        "실장",
        "수습사원",
        "선임",
        "책임",
        "수석",
        "반장",
        "공장장",
        "대표",
    ]

    # 텍스트 전처리
    processed_sentence = re.sub("[ ]", "/", sentence)

    # 한국어 문장 쪼개기
    kor_split_list = processed_sentence.split("/")

    flag = 0
    eng_split_list = []

    # 구글 영어 번역 & 문장 쪼개기, 서버 여러개 중 하나 쓰기
    for num in range(9, -1, -1):
        if flag == 1:
            continue

        eng_sentence = get_translate(sentence, "ko", "en", num)

        if eng_sentence != 429:
            eng_split_list = eng_sentence.split("/")
            flag = 1

    ans_idx = int()
    flag = 0

    for text_idx, text in enumerate(eng_split_list):

        # 먼저 job_list에서 서치
        for job_title in job_list:
            # flag가 1이면 이후 수행 x
            if flag == 1:
                break

            # job_list 내부에서 서치
            if job_title in kor_split_list[text_idx]:
                flag = 1
                ans_idx = text_idx

        if flag == 1:
            return kor_split_list[ans_idx]

        # job_list에서 존재하지 않는다면 finder 사용
        else:
            try:
                output = finder.findall(text)
                ans_idx = text_idx
                return kor_split_list[ans_idx]
            except:
                continue


def extract_info(texts, tags, finder):
    info_dict = {"LOC": [], "PER": [], "ORG": [], "JOB": []}
    other_text = ""

    per_name = ""
    loc_name = ""
    org_name = ""

    for idx, text in enumerate(texts):

        # 샾 제거
        processed_text = re.sub("[#]", "", text)
        # 띄어쓰기 변경
        processed_text = re.sub("[_]", " ", processed_text)

        if tags[idx] != "O":

            if tags[idx][2:] == "PER":

                if tags[idx][0] == "B":
                    per_name += " " + processed_text
                else:
                    per_name += processed_text

            elif tags[idx][2:] == "LOC":

                if tags[idx][0] == "B":
                    loc_name += " " + processed_text
                else:
                    loc_name += processed_text

            elif tags[idx][2:] == "ORG":

                if tags[idx][0] == "B":
                    org_name += " " + processed_text
                else:
                    org_name += processed_text

        #             temp = '-'*(10 - len(texts[idx]))

        #             print(f'{texts[idx]} {temp} {tags[idx]}')
        # O에 해당되는 것들 전부 모으기
        else:
            other_text += processed_text

    # 중복 공백 제거
    other_text = re.sub(" +", "/", other_text)

    job_name = detect_job(other_text, finder)

    info_dict["PER"].append(per_name.strip())
    info_dict["LOC"].append(loc_name.strip())
    info_dict["ORG"].append(org_name.strip())
    info_dict["JOB"].append(job_name)

    return info_dict

