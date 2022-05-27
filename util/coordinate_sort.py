import numpy as np
from typing import Dict,List, DefaultDict
from collections import defaultdict

def get_avail_range(y_point:int)->List:
    """
    파라미터 값 기준으로 ±2% 범위의 리스트를 생성합니다.

    parameter 
        y_point : 글자의 왼쪽 아래 y 좌표 값
    return
        y_point 기준 ±2% 범위 리스트(int 형)
    """
    ret = np.arange(y_point-y_point*0.02, y_point+y_point*0.02, 1)
    ret = np.asarray(ret, dtype=int).tolist()

    return ret

def divide_sector(word_dict:Dict)->DefaultDict:
    """
    y 값으로 정렬된 딕셔너리들을 y 값에 따라 섹터를 구분 짓습니다.
    어떤 한 글자의 왼쪽 아래 y 좌표 값이 다른 글자의 y 좌표의 ±2% 안에 포함된다면
    같은 섹터로 구분 지어줍니다.

    parameter
        word_dict : y 좌표를 기준으로 정렬이 완료된 딕셔너리 형태
    return
        섹터가 구분지어진 defaultdict(list) 형태
        담고있는 정보 : {섹터 ID : [{points:[List]}, {text:str}]}
    """
    sector = defaultdict(list)

    for dat in word_dict:
        y_point = dat["points"][3][1]
        avail_y_points = get_avail_range(y_point=y_point) 

        sec_key = None

        for sec in avail_y_points:
            if sec in sector.keys():
                sec_key = sec

        if not sec_key:
            sec_key = y_point
        
        sector[sec_key].append({"text":dat['text'], "points":dat['points']})

    return sector

def sort_by_y(api_output):
    """
    OCR API 를 거쳐 나온 값들을 y 값에 따라 정렬합니다. 

    parameter
        api_output : 이미지를 OCR API 에 넣어 나온 결과값
    return 
        y 값을 기준으로 정렬된 딕셔너리 형태    
    """
    ret = sorted(api_output['ocr']['word'], key=lambda k: [k['points'][3][1], k['points'][3][0]])

    return ret

def sort_by_x(sector:DefaultDict)->DefaultDict:
    """
    섹터 구분이 된 디폴트 딕셔너리를 좌표 값 중 오른쪽 위의 x 값으로 다시 정렬합니다.

    parameter
        sector : y 값에 따른 정렬과 섹터 구분이 완료된 defaultdict
    return
        x 값 정렬까지 완료된 defaultdict 
    """
    for key in sector.keys():
        sector[key] = sorted(sector[key], key=lambda k:k['points'][0][0])

    return sector

def coordinate_sort_with_sector(api_output):
    ret = sort_by_y(api_output)
    ret = divide_sector(ret) 
    ret = sort_by_x(ret)
    
    return ret