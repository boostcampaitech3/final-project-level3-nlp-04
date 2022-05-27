import pickle


def save_preprocessed_data(data):

    with open("token.pkl", "wb") as f:
        pickle.dump(data[0], f)
    with open("tag.pkl", "wb") as f:
        pickle.dump(data[1], f)


def load_preprocessed_data():

    with open("token.pkl", "rb") as f:
        token_docs = pickle.load(f)
    with open("tag.pkl", "rb") as f:
        tag_docs = pickle.load(f)

    return token_docs, tag_docs

def save_tag2id(data):
    with open("tag2id.pkl", "wb") as f:
        pickle.dump(data, f)

def load_tag2id():
    with open("tag2id.pkl", "rb") as f:
        tag2id = pickle.load(f)
    
    return tag2id