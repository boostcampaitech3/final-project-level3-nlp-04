import pandas as pd
from collections import deque
from coordinate_sort import *
from typing import DefaultDict, Tuple, List 
from preprocess_info import *
from pykospacing import Spacing



def is_box_overlap(origin:List[Tuple[float, float]],target:List[Tuple[float, float]])->bool:
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
        if min_x<=x and x<=max_x and min_y<=y and y<=max_y:
            return True

    return False

def extend_box(data:Dict)->List:
    extend_list = []  
    weight_x = 0.12 # 늘리는 비율 (수정해야되는 값)
    w_x_1 = 1 + weight_x
    w_x_2 = 1 - weight_x

    weight_y = 0.15
    w_y_1 = 1+weight_y
    w_y_2 = 1-weight_y

    x_w = [w_x_2,w_x_1,w_x_1,w_x_2]
    y_w = [w_y_1,w_y_1,w_y_2,w_y_2]
    
    for idx, point in enumerate(data['points']):
        extend_list.append([point[0] * x_w[idx], point[1] * y_w[idx]])

    return extend_list 

def get_box_info(data_dict:DefaultDict)->Tuple[List, List]:
    text_list = []
    box_list = []

    for key in data_dict.keys():
        data_list = data_dict[key]

        for data in data_list:
            box_list.append(extend_box(data))
            text_list.append(data['text'])

    return box_list, text_list

def sector_bfs(box_list:List)->List:
    graph = [[] for _ in range(len(box_list))]

    for i, origin in enumerate(box_list):
        for j, target in enumerate(box_list):
            if i >= j :
                continue
            if is_box_overlap(origin,target):
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

def get_serialization_string(api_output:Dict)->DefaultDict:

    data_dict = coordinate_sort_with_sector(api_output)
    box_list, text_list = get_box_info(data_dict)
    sector_list = sector_bfs(box_list)

    bc_df = pd.DataFrame({'text':text_list,'cluster':sector_list})
    bc_df.sort_values(by=['cluster'],axis=0,kind='mergesort',inplace=True)


    serialized_text = defaultdict(list)

    for i in range(len(bc_df)):
        key = bc_df.loc[i, 'cluster']
        text = preprocess_text(bc_df.loc[i, 'text'])

        serialized_text[key].append(text)

    serialized_text = detect_phone(serialized_text)
    serialized_text = detect_email(serialized_text)
    serialized_text = detect_company(serialized_text)
    spacing = Spacing()

    for key in serialized_text.keys():
        if type(key) != str:
            spacing_text = "".join(serialized_text[key])
            spacing_text = spacing(spacing_text)        
            serialized_text[key] = spacing_text

    serialized_text = remove_empty_list(serialized_text)
    return serialized_text 
