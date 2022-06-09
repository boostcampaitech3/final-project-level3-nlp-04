import re
from collections import OrderedDict
from extraction.detection import detect_job
from typing import List


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


def remove_duplicate_output(output: str):
    ret = ""

    origin = output.split()
    for word in origin:
        if not word in ret:
            ret += word
            ret += " "

    return ret.strip()


def get_final_output(output):
    scan_fail = "Scan Failed"
    new_output = OrderedDict(
        {
            "이름": scan_fail,
            "직책": scan_fail,
            "회사명": scan_fail,
            "주소": scan_fail,
            "전화번호": scan_fail,
            "이메일": scan_fail,
        }
    )

    new_output["회사명"] = (
        remove_duplicate_output(output["ORG"][0]).strip()
        if output["ORG"][0] != ""
        else scan_fail
    )
    new_output["주소"] = (
        remove_duplicate_output(output["LOC"][0]).strip()
        if output["LOC"][0] != ""
        else scan_fail
    )
    new_output["이름"] = (
        remove_duplicate_output(output["PER"][0]).strip()
        if output["PER"][0] != ""
        else scan_fail
    )
    new_output["직책"] = (
        output["JOB"][0].strip()
        if output["JOB"][0] != "" and output["JOB"][0]
        else scan_fail
    )
    new_output["전화번호"] = output["phone"].strip() if output["phone"] != "" else scan_fail
    new_output["이메일"] = output["email"].strip() if output["email"] != "" else scan_fail

    return new_output


def ensemble(outputs: List[OrderedDict]) -> OrderedDict:
    name_list = ""
    job_title_list = ""
    company_list = ""
    location_list = ""
    phone_list = ""
    email_list = ""

    (
        ensemble_name,
        ensemble_job,
        ensemble_company,
        ensemble_loc,
        ensemble_phone,
        ensemble_email,
    ) = ("", "", "", "", "", "")

    for output in outputs:
        if output["이름"] != "Scan Failed" and len(output["이름"]) > 1:
            name_list += f'{output["이름"]} '
        if output["직책"] != "Scan Failed" and len(output["직책"]) > 1:
            job_title_list += f'{output["직책"]} '
        if output["회사명"] != "Scan Failed" and len(output["회사명"]) > 1:
            company_list += f'{output["회사명"]} '
        if output["주소"] != "Scan Failed" and len(output["주소"]) > 1:
            location_list += f'{output["주소"]} '
        if output["전화번호"] != "Scan Failed" and len(output["전화번호"]) > 1:
            phone_list += f'{output["전화번호"]} '
        if output["이메일"] != "Scan Failed" and len(output["이메일"]) > 1:
            email_list += f'{output["이메일"]} '

    name_list = name_list.strip().split()
    job_title_list = job_title_list.strip().split()
    company_list = company_list.strip().split()
    location_list = location_list.strip().split()
    phone_list = phone_list.strip().split()
    email_list = email_list.strip().split()

    if not name_list:
        name_list.append("Scan Failed")
    if not job_title_list:
        job_title_list.append("Scan Failed")
    if not company_list:
        company_list.append("Scan Failed")
    if not location_list:
        location_list.append("Scan Failed")
    if not phone_list:
        phone_list.append("Scan Failed")
    if not email_list:
        email_list.append("Scan Failed")

    for name in name_list:
        if len(list(set(name_list))) == 1:
            ensemble_name = name
            break
        if name_list.count(name) > 1 and name not in ensemble_name and len(name) > 1:
            ensemble_name += f"{name} "

    for job in job_title_list:
        if len(list(set(job_title_list))) == 1:
            ensemble_job = job
            break
        if job_title_list.count(job) > 1 and job not in ensemble_job and len(job) > 1:
            ensemble_job += f"{job} "

    for company in company_list:
        if len(list(set(company_list))) == 1:
            ensemble_company = company
            break
        if (
            company_list.count(company) > 1
            and company not in ensemble_company
            and len(company) > 1
        ):
            ensemble_company += f"{company} "

    for loc in location_list:
        if len(list(set(location_list))) == 1:
            ensemble_loc = loc
            break
        if location_list.count(loc) > 1 and loc not in ensemble_loc and len(loc) > 1:
            ensemble_loc += f"{loc} "

    for phone in phone_list:
        if len(list(set(phone_list))) == 1:
            ensemble_phone = phone
            break
        if (
            phone_list.count(phone) > 1
            and phone not in ensemble_phone
            and len(phone) > 1
        ):
            ensemble_phone += f"{phone} "

    for email in email_list:
        if len(list(set(email_list))) == 1:
            ensemble_email = email
            break
        if (
            email_list.count(email) > 1
            and email not in ensemble_email
            and len(email) > 1
        ):
            ensemble_email += f"{email} "

    ensemble_name = name_list[0] if ensemble_name == "" else ensemble_name.strip()
    ensemble_loc = location_list[0] if ensemble_loc == "" else ensemble_loc.strip()
    ensemble_company = (
        company_list[0] if ensemble_company == "" else ensemble_company.strip()
    )
    ensemble_job = job_title_list[0] if ensemble_job == "" else ensemble_job.strip()
    ensemble_email = email_list[0] if ensemble_email == "" else ensemble_email.strip()
    ensemble_phone = phone_list[0] if ensemble_phone == "" else ensemble_phone.strip()

    ensemble_output = OrderedDict(
        {
            "이름": ensemble_name,
            "직책": ensemble_job,
            "회사명": ensemble_company,
            "주소": ensemble_loc,
            "전화번호": ensemble_phone,
            "이메일": ensemble_email,
        }
    )

    return ensemble_output
