import re
# 모듈화 코드 작성(파파고)
import googletrans
import urllib.request
import json
import requests

client_id_list = ['jsTjNqkZfI7vfZhyx3BZ', 'onbDQLsfFQJnUANZVKpM', '1_HmWOIMkrY_QfNOYWQl','PZFMK_CGszrBZDgP5pSd', 'PvbiQ8pMeOk8q4sRCJA0', 
                 '3rCf3GEd3fvtEV6Vvh2w', 'fn7xQVUTJv8aot7uTQro', 'pHwYN8y2A6Y03gt9IfT3','WdLufJEZi2lPAEfvKL15','NxyyDoXdqruDuAHJBR5u']

client_secret_list = ['GGxUC1wMbj','PSRQa_fh9F','7iAPCQdOH9','uOLwEF3UOt', 'wVoIpNeGns',
                     '29491wg_uX', 'bOwpDCZhUz','8SMSp4oIWV','HW47_dHuQg','9DA9gXJAAG']


def get_translate(text,lan1, lan2, num):
    
    data = {'text' : text,
            'source' : lan1,
            'target': lan2}
    
    url = "https://openapi.naver.com/v1/papago/n2mt"

    header = {"X-Naver-Client-Id":client_id_list[num],
              "X-Naver-Client-Secret":client_secret_list[num]}

    response = requests.post(url, headers=header, data= data)
    rescode = response.status_code

    if rescode==200 :
        t_data = response.json()
        return t_data['message']['result']['translatedText']
    else:
        return rescode
                      
def find_job(sentence) :
    # global eng_split_list
    
    # 기본적인 Rule-Base 병행
    job_list = ['매니저', '회장', '사장','전무','상무','이사','부장','차장','과장','계장','대리','주임','사원',
                '인턴','본부장','지점장','행장','부행장','실장','수습사원','선임','책임','수석','반장','공장장']
    
    # 텍스트 전처리
    processed_sentence = re.sub('[ ]', '/', sentence)
    
    # 한국어 문장 쪼개기
    kor_split_list = processed_sentence.split("/")
    
    flag = 0
    eng_split_list = []
    
    # 구글 영어 번역 & 문장 쪼개기, 서버 여러개 중 하나 쓰기
    for num in range(9,-1,-1) : 
        if flag == 1 : 
            continue
        
        eng_sentence =  get_translate(sentence, 'ko','en', num)
        
        if eng_sentence != 429 : 
            eng_split_list = eng_sentence.split("/")
            flag = 1
            
    ans_idx = int()
    flag = 0
    
    for text_idx, text in enumerate(eng_split_list) : 
        
        # 먼저 job_list에서 서치
        for job_title in job_list : 
            # flag가 1이면 이후 수행 x
            if flag == 1 : 
                break
            
            # job_list 내부에서 서치
            if job_title in kor_split_list[text_idx] : 
                flag = 1
                ans_idx = text_idx

        if flag == 1 : 
            return kor_split_list[ans_idx]

        # job_list에서 존재하지 않는다면 finder 사용
        else : 
            try : 
                output = finder.findall(text)
                ans_idx = text_idx
                return kor_split_list[ans_idx]
            except :
                continue


# 문장에서 이름, 주소, 단체, 직책 찾기
def extract_info(texts, tags, finder):
    info_dict = {'LOC': [], 'PER': [], 'ORG': [],'JOB': []}
    other_text = ''
    
    per_name = ''
    loc_name = ''
    org_name = ''
    
    for idx, text in enumerate(texts) :
        
        # 샾 제거
        processed_text = re.sub('[#]','',text)
        # 띄어쓰기 변경
        processed_text = re.sub('[_]',' ',processed_text)
        
        if tags[idx] != 'O' : 
            
            if tags[idx][2:] == 'PER' : 
                
                if tags[idx][0] == 'B' : 
                    per_name += (' ' + processed_text)
                else : 
                    per_name += processed_text
                
            elif tags[idx][2:] == 'LOC' : 
                
                if tags[idx][0] == 'B' : 
                    loc_name += (' ' + processed_text)
                else : 
                    loc_name += processed_text
            
            elif tags[idx][2:] == 'ORG' : 
                
                if tags[idx][0] == 'B' : 
                    org_name += (' ' + processed_text)
                else : 
                    org_name += processed_text
            
#             temp = '-'*(10 - len(texts[idx]))
    
#             print(f'{texts[idx]} {temp} {tags[idx]}')
        # O에 해당되는 것들 전부 모으기
        else : 
            other_text += processed_text
    
    # 중복 공백 제거
    other_text = re.sub(' +','/',other_text)
    
    job_name = find_job(other_text)
    
    info_dict['PER'].append(per_name[1:])
    info_dict['LOC'].append(loc_name[1:])
    info_dict['ORG'].append(org_name)
    info_dict['JOB'].append(job_name)
    
    return info_dict