import numpy as np
import re
from typing import Dict, List, DefaultDict, Tuple
from collections import defaultdict
import pandas as pd
from collections import deque
from pykospacing import Spacing
import sys
sys.path.append("../")
from preprocess.cleansing import *
from extraction.detection import *

"""
Serialization에 필요한 함수 Module
"""


def get_avail_range(y_point: int) -> List:
    """
    파라미터 값 기준으로 ±2% 범위의 리스트를 생성합니다.

    parameter 
        y_point : 글자의 왼쪽 아래 y 좌표 값
    return
        y_point 기준 ±2% 범위 리스트(int 형)
    """
    ret = np.arange(y_point - y_point * 0.02, y_point + y_point * 0.02, 1)
    ret = np.asarray(ret, dtype=int).tolist()

    return ret


def divide_sector(word_dict: Dict) -> DefaultDict:
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

        sector[sec_key].append({"text": dat["text"], "points": dat["points"]})

    return sector


def sort_by_y(api_output: Dict) -> Dict:
    """d
    OCR API 를 거쳐 나온 값들을 y 값에 따라 정렬합니다. 

    parameter
        api_output : 이미지를 OCR API 에 넣어 나온 결과값
    return 
        y 값을 기준으로 정렬된 딕셔너리 형태    
    """
    ret = sorted(
        api_output["ocr"]["word"], key=lambda k: [k["points"][3][1], k["points"][3][0]]
    )

    return ret


def sort_by_x(sector: DefaultDict) -> DefaultDict:
    """
    섹터 구분이 된 디폴트 딕셔너리를 좌표 값 중 오른쪽 위의 x 값으로 다시 정렬합니다.

    parameter
        sector : y 값에 따른 정렬과 섹터 구분이 완료된 defaultdict
    return
        x 값 정렬까지 완료된 defaultdict 
    """
    for key in sector.keys():
        sector[key] = sorted(sector[key], key=lambda k: k["points"][0][0])

    return sector


def coordinate_sort_with_sector(api_output: Dict) -> DefaultDict:  # 좌표 기반으로 sector sort
    ret = sort_by_y(api_output)
    ret = divide_sector(ret)
    ret = sort_by_x(ret)

    return ret


def is_box_overlap(
    origin: List[Tuple[float, float]], target: List[Tuple[float, float]]
) -> bool:
    x_list = []
    y_list = []
    for x, y in origin:
        x_list.append(x)
        y_list.append(y)
    max_x = max(x_list)
    min_x = min(x_list)
    max_y = max(y_list)
    min_y = min(y_list)

    for x, y in target:
        if min_x <= x and x <= max_x and min_y <= y and y <= max_y:
            return True

    return False


def extend_box(data: Dict) -> List:
    extend_list = []
    weight_x = 0.12  # 늘리는 비율 (수정해야되는 값)
    w_x_1 = 1 + weight_x
    w_x_2 = 1 - weight_x

    weight_y = 0.15
    w_y_1 = 1 + weight_y
    w_y_2 = 1 - weight_y

    x_w = [w_x_2, w_x_1, w_x_1, w_x_2]
    y_w = [w_y_1, w_y_1, w_y_2, w_y_2]

    for idx, point in enumerate(data["points"]):
        extend_list.append([point[0] * x_w[idx], point[1] * y_w[idx]])

    return extend_list


def get_box_info(data_dict: DefaultDict) -> Tuple[List, List]:
    text_list = []
    box_list = []

    for key in data_dict.keys():
        data_list = data_dict[key]

        for data in data_list:
            box_list.append(extend_box(data))
            text_list.append(data["text"])

    return box_list, text_list


def sector_bfs(box_list: List) -> List:
    graph = [[] for _ in range(len(box_list))]

    for i, origin in enumerate(box_list):
        for j, target in enumerate(box_list):
            if i >= j:
                continue
            if is_box_overlap(origin, target):
                graph[i].append(j)
                graph[j].append(i)

    sector_list = [-1 for _ in range(len(box_list))]
    sector_idx = 0

    for i in range(len(graph)):
        if sector_list[i] == -1:
            que = deque()
            que.append(i)
            sector_list[i] = sector_idx

            while que:
                now = que.pop()
                for next in graph[now]:
                    if sector_list[next] == -1:
                        sector_list[next] = sector_idx
                        que.append(next)

            sector_idx += 1

    return sector_list


def get_serialization_string(api_output: Dict) -> DefaultDict:

    data_dict = coordinate_sort_with_sector(api_output)
    box_list, text_list = get_box_info(data_dict)
    sector_list = sector_bfs(box_list)

    bc_df = pd.DataFrame({"text": text_list, "cluster": sector_list})
    bc_df.sort_values(by=["cluster"], axis=0, kind="mergesort", inplace=True)

    serialized_text = defaultdict(list)

    for i in range(len(bc_df)):
        key = bc_df.loc[i, "cluster"]
        text = cleaning_special_token(bc_df.loc[i, "text"])

        serialized_text[key].append(text)

    serialized_text = detect_phone(serialized_text)
    serialized_text = detect_email(serialized_text)
    spacing = Spacing()

    for key in serialized_text.keys():
        if type(key) != str:
            spacing_text = "".join(serialized_text[key])
            spacing_text = spacing_text.replace(" ", "") 
            spacing_text = spacing_text.upper()
            spacing_text = spacing(spacing_text)
            serialized_text[key] = spacing_text

    serialized_text = remove_empty_list(serialized_text)
    return serialized_text

