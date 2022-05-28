from collections import defaultdict
from typing import DefaultDict, List
import itertools
import re

def preprocess_text(text:str)->str:
    special = ["#", "$", "%", "&", "*", "(", ")", ":", "-", "<", ">", "|"]

    for token in special:
        text = text.replace(token, "")
    
    text = text.replace("+82 ", "0") 

    return text.lower()

def remove_duplicate(serialized:DefaultDict, target_list:List[int]):
    idx_list = []

    for val in serialized.values():
        temp = []
        for idx, v in enumerate(val):
            for num in target_list:
                if v in num:
                    temp.append(idx)
        idx_list.append(list(set(temp)))

    for idx, (key,val) in enumerate(serialized.items()):
        for remove_idx in idx_list[idx]:
            val[remove_idx] = None
        serialized[key] = list(filter(None, val))
    return serialized

def detect_phone(serialized:DefaultDict)->DefaultDict:
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
    phone_list = list(filter(lambda x : x.startswith("010"), phone_list))
    serialized["phone"].extend(phone_list)

    return serialized

def preprocess_domain(text:str)->str:
    domains = ["co", "com", "kr", "ne", "net", "or"]

    text = text.replace(".", "").strip()

    for domain in domains:
        if text == domain:
            return f".{domain}" 

    return text 

def detect_email(serialized:DefaultDict)->DefaultDict:
    stack = []
    email_list = []
    p = re.compile('^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')

    for val in itertools.chain.from_iterable(serialized.values()):
        if p.match(val):
            email_list.append(val)
            break

        stack.append(val)
        val = preprocess_domain(val)

        if '@' in stack[-1]:
            stack.clear()
            stack.append(val)
        elif len(stack) > 1 and '@' in stack[-2]:
            temp = stack[-2]
            stack.clear()
            stack.append(temp+val)

        if p.match(stack[-1]):
            email_list.append(stack[-1])
            break

    serialized = remove_duplicate(serialized, email_list)
    serialized["email"].extend(email_list)

    return serialized

def detect_company(serialized:DefaultDict)->DefaultDict:
    company_related_sector = [0,1,2]
    company_list = []


    for key in company_related_sector:
        for text in serialized[key]:
            text = preprocess_text(text)
            company_list.append(text.upper())

    serialized = remove_duplicate(serialized, company_list)
    company = " ".join(company_list)
    serialized["company"].append(company)

    return serialized

def remove_empty_list(serialized:DefaultDict)->DefaultDict:
    new_serialized = defaultdict(str)

    for k,v in serialized.items():
        if v != '' and type(v) == str:
            new_serialized[k] = v
        
        if type(v) == list and v:
            new_serialized[k] = v[0]

    return new_serialized