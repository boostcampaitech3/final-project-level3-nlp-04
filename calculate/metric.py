import Levenshtein as Lev
import pandas as pd
from typing import Dict, Tuple, List
from sklearn.metrics import f1_score, recall_score, precision_score
import pprint
import sys
sys.path.append("../")
from preprocess.cleansing import cleaning_special_token
"""
category-level f1 score
    - precision :  (그 중 실제 데이터에 있는 정보 수)/(모델이 추출한 정보 수)
    - recall : (그 중 모델이 맞춘 정보 수)/(실제 데이터에 있는 정보 수)

실제 데이터(y_true)의 경우, 정보가 들어있는 경우 1, 아닌 경우 0으로 표현하면 됨
그렇다면, 모델이 예측한 정보는 어떻게 해야 할까?
OCR로 값을 거치는 것이기 때문에 모델이 예측한 답이 불완전할 수밖에 있음. 그렇다면 여기에 Character Error Rate (CER) 개념을 적용하는 건 어떨까?
모델이 값을 추출하더라도, 그 값의 Error 값이 높다면 그 값은 못 맞춘 값이라 생각하자.
그 기준은 주관적일 수 밖에 없는데,, 일단은 10%라고 하자. Error 값이 높지 않다면 그것은 맞춘 정보라고 하자.
 """

def cer(ref: str, hyp: str) -> Tuple[int, int, int]:
    hyp = hyp.replace(' ', '')
    ref = cleaning_special_token(ref)

    dist = Lev.distance(hyp, ref)
    length = len(ref)

    return dist, length, dist/length


def calculate_metric(y_true: Dict[str, str], y_pred: Dict[str, str], threshold: int = 0.3) -> Dict[str, int]:

    y_true_value = [x for x in y_true.values()]
    y_pred_value = [x for x in y_pred.values()]

    y_true_bin = [1 if x != 'Scan Failed' else 0 for x in y_true_value]
    y_pred_bin = []

    for ref, hyp in zip(y_true_value, y_pred_value):
        pprint.pprint(f"TRUE : {ref} / PRED : {hyp}")
        if cer(ref, hyp)[2] <= threshold:
            if hyp == "Scan Failed":
               y_pred_bin.append(0) 
            else:
                y_pred_bin.append(1)
        else:
            y_pred_bin.append(0)

    answer = {"f1_score": f1_score(y_true_bin, y_pred_bin),
              "precision": precision_score(y_true_bin, y_pred_bin),
              "recall": recall_score(y_true_bin, y_pred_bin)}

    return answer

# image-level accuracy : 이미지내에 모든 필요 정보를 찾은 비율
# 하나의 이미지 정보에서 f1_score가 1(모든 정보를 오탈자 없이 완벽하게 찾은 경우)이면 가장 좋겠지만 현실적으로 그러기란 쉽지 않음.
# 그렇다면 f1_score 값이 일정 기준을 넘었을 때 모든 정보를 찾은 것으로 가정하는 것은 어떨까? 0.8?? 은 어떠한지..?


def make_true_list(path: str) -> List[Dict[str, str]]:
    
    df = pd.read_csv(path, index_col=0)

    true_list = []
    for idx in range(len(df)):
        true_list.append(dict(df.iloc[idx]))

    return true_list


def calculate_accuracy(true_list: List[Dict[str, str]], pred_list: List[Dict[str, str]], threshold: int = 0.6) -> int:
    cnt = 0
    for y_true, y_pred in zip(true_list, pred_list):
        metric = calculate_metric(y_true, y_pred)
        if metric['f1_score'] >= threshold:
            cnt += 1
        pprint.pprint(metric)
        print()

    return cnt/len(true_list)