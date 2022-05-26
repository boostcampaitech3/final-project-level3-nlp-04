import pickle


def save_preprocessed_data(save_path: str, data):

    with open("list.pickle", "wb") as f:
        pickle.dump(data, f)


def load_preprocessed_data(save_path: str):

    with open("list.pickle", "rb") as f:
        data = pickle.load(f)
    return data
