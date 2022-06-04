import re
from collections import OrderedDict
from extraction.detection import detect_job

def extract_info(texts, tags, finder):
    info_dict = {"LOC": [], "PER": [], "ORG": [], "JOB": []}
    other_text = ""

    per_name = ""
    loc_name = ""
    org_name = ""
    has_number = lambda x: any(elem.isdigit() for elem in x)

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
                if has_number(processed_text):
                    continue
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

def remove_duplicate_output(output:str):
    ret = ""

    origin = output.split()
    for word in origin:
        if not word in ret:
            ret += word
            ret += " "

    return ret.strip()

def get_final_output(output):
    scan_fail = "Scan Failed"
    new_output = OrderedDict({"이름":scan_fail, "직책":scan_fail, "회사명": scan_fail, "주소":scan_fail, "전화번호":scan_fail, "이메일":scan_fail})

    new_output["회사명"]=remove_duplicate_output(output["ORG"][0]) if output["ORG"][0]!='' else scan_fail
    new_output["주소"]=remove_duplicate_output(output["LOC"][0]) if output["LOC"][0]!='' else scan_fail
    new_output["이름"]=remove_duplicate_output(output["PER"][0]) if output["PER"][0]!='' else scan_fail
    new_output["직책"]=output["JOB"][0] if output["JOB"][0]!='' and output['JOB'][0] else scan_fail
    new_output["전화번호"]=output["phone"] if output["phone"] != "" else scan_fail
    new_output["이메일"]=output["email"] if output["email"] != "" else scan_fail

    return new_output