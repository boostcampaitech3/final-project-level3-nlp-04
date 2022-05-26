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
