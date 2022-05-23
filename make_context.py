import pandas as pd
import json
from collections import deque
from coordinate_sort_copy import *

def isCross(origin,target):
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

with open('/opt/ml/final/output/vflat_image_1.json') as f:
    json_data = json.load(f)

data_dict = coordinate_sort_with_sector(json_data)

def get_context(data_dict):

    def make_box(data_dict):
        text_list = []
        box_list = []
        avg_x_list = []
        avg_y_list = []
        for key in data_dict.keys():
            data_list = data_dict[key]

            for data in data_list:
                point_list = []  
                w = 0.09 # 수정해야하는 값
                w1 = 1 + w
                w2 = 1 - w
                x_w = [w2,w1,w2,w1]
                y_w = [w2,w2,w1,w1]
                sum_x = 0
                sum_y = 0
                
                for idx, point in enumerate(data['points']):
                    sum_x += point[0]
                    sum_y += point[1]
                    point_list.append((point[0] * x_w[idx], point[1] * y_w[idx]))
                    
                box_list.append(point_list)
                text_list.append(data['text'])
                avg_x_list.append(sum_x/4)
                avg_y_list.append(sum_y/4)
        return box_list, text_list, avg_x_list, avg_y_list

    def sector_bfs(box_list):

        graph = [[] for _ in range(len(box_list))]

        for i, origin in enumerate(box_list):
            for j, target in enumerate(box_list):
                if i >= j :
                    continue
                if isCross(origin,target):
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

    box_list, text_list, avg_x_list, avg_y_list = make_box(data_dict)
    sector_list = sector_bfs(box_list)
    bc_df = pd.DataFrame({'text':text_list,'x':avg_x_list,'y':avg_y_list,'cluster':sector_list})
    bc_df.sort_values(by=['cluster'],axis=0,kind='mergesort',inplace=True)
    context = list(bc_df.loc[:, 'text'])
    print(context)
    return context

context = get_context(data_dict)
