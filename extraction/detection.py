from typing import DefaultDict
import itertools
import re
import sys

sys.path.append("../")
from preprocess.cleansing import *
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
    phone_list = list(
        filter(lambda x: x.startswith("010") or x.startswith("011"), phone_list)
    )
    serialized["phone"].extend(phone_list)

    return serialized


def detect_email(serialized: DefaultDict) -> DefaultDict:
    stack = []
    email_list = []
    p = re.compile("^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")

    for val in itertools.chain.from_iterable(serialized.values()):
        if p.match(val) and not val.endswith("co"):
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
            if stack[-1].endswith("co"):
                continue
            email_list.append(stack[-1])
            break

    serialized = remove_duplicate(serialized, email_list)
    serialized["email"].extend(email_list)

    return serialized


def detect_job(sentence, finder):
    # 기본적인 Rule-Base 병행
    job_list = [
        "매니저",
        "매니져",
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
        "팀장",
        "검사",
        "국장",
        "센터장",
        "주무관",
        "입학사정관",
        "디자이너",
        "지부장",
        "오토플래너",
    ]

    # 텍스트 전처리
    sentence = re.sub("[-=+,#/\?:^$.@*\"※~&%ㆍ!』\\'|\(\)\[\]\<\>`'…》]", " ", sentence)
    processed_sentence = re.sub("[ ]", "/", sentence)

    # 한국어 문장 쪼개기
    kor_split_list = processed_sentence.split("/")
    # print(kor_split_list)

    flag = 0
    eng_split_list = []

    for text_idx, text in enumerate(kor_split_list):

        # Rule-Base 탐색(job_list)
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
        # 구글 영어 번역 & 문장 쪼개기, 서버 여러개 중 하나 쓰기
        for num in range(9, -1, -1):
            if flag == 1:
                continue

            eng_sentence = get_translate(processed_sentence, "ko", "en", num)
            if eng_sentence != 429:
                eng_split_list = eng_sentence.split("/")
                flag = 1

        ans_idx = int()
        flag = 0

        for idx, text in enumerate(eng_split_list):

            if flag == 1:
                break
            input_text = text.strip()
            try:
                output = finder.findall(input_text)
                ans_idx = idx
                flag = 1
            except:
                continue

        if flag == 1:
            return kor_split_list[ans_idx]

        else:
            false_text = ""
            return false_text
