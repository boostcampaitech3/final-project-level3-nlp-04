from typing import DefaultDict, List
from collections import defaultdict

"""
text cleaning을 위한 함수 Module
"""


def cleaning_special_token(text: str) -> str:
    text = text.lower()
    special = ["#", "$", "%", "&", "*", "(", ")", ":", "-", "<", ">", "|", "tel", "fax", "mobile", "email", "e-mail"]

    for token in special:
        text = text.replace(token, "")

    text = text.replace("+82", "0")
    text = text.replace("+82 ", "0")

    return text


def remove_duplicate(serialized: DefaultDict, target_list: List[int]):
    idx_list = []

    for val in serialized.values():
        temp = []
        for idx, v in enumerate(val):
            for num in target_list:
                if v in num:
                    temp.append(idx)
        idx_list.append(list(set(temp)))

    for idx, (key, val) in enumerate(serialized.items()):
        for remove_idx in idx_list[idx]:
            val[remove_idx] = None
        serialized[key] = list(filter(None, val))
    return serialized


def cleaning_domain(text: str) -> str:
    domains = ["co", "com", "kr", "ne", "net", "or"]

    text = text.replace(".", "").strip()

    for domain in domains:
        if text == domain:
            return f".{domain}"

    return text


def remove_empty_list(serialized: DefaultDict) -> DefaultDict:
    new_serialized = defaultdict(str)

    for k, v in serialized.items():
        if v != "" and type(v) == str:
            new_serialized[k] = v

        if type(v) == list and v:
            new_serialized[k] = v[0]

    return new_serialized