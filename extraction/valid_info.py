import re
from extraction.detection import detect_job

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