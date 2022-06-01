import pickle

def save_tag2id(data):
    with open("/opt/ml/final/model/tag2id.pkl", "wb") as f:
        pickle.dump(data, f)

def load_tag2id():
    with open("/opt/ml/final/model/tag2id.pkl", "rb") as f:
        tag2id = pickle.load(f)
    
    return tag2id