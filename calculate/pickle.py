import pandas as pd
import os
import cv2
import pickle

def save_pred_pickle(callback_fn, model, tokenizer, device, finder):
    pred = []
    df = pd.read_csv("./data_info.csv")

    idx = 0  
    for file_path in df['파일명'].values:
        img = cv2.imread(os.path.join("/opt/ml/final/data/image", f"{file_path}.jpg"))
        imgdata = cv2.imencode('.PNG', img)[1].tobytes()
        print(f"{idx} : {file_path}")
        idx += 1
        content = callback_fn(img=imgdata, model=model, tokenizer=tokenizer, device=device, finder=finder)

        pred.append(content)

    with open("./pred.pkl", "wb") as f:
        pickle.dump(pred, f)    

def load_pred_pickle():
    with open("./pred.pkl", "rb") as f:
        pred= pickle.load(f)
    
    return pred  