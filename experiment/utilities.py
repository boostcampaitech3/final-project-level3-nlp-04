import re
import os
import glob
from pathlib import Path


def load_file(file_path="/opt/ml/NER"):
    file_list = []
    for x in os.walk(file_path):
        for y in glob.glob(os.path.join(x[0], "*_NER.txt")):  # ner.*, *_NER.txt
            file_list.append(y)

    return file_list


def read_file(
    file_list,
):  # 이중 엔터를 기준으로 document 로써 구분을 하게 됨. 각 라인을 읽어나가면서 토큰들을 문장으로 붙여나가는 과정을 거칠 것임.
    token_docs = []
    tag_docs = []
    for file_path in file_list:
        # print("read file from ", file_path)
        file_path = Path(file_path)
        raw_text = file_path.read_text().strip()
        raw_docs = re.split(r"\n\t?\n", raw_text)
        for doc in raw_docs:
            tokens = []
            tags = []
            for line in doc.split("\n"):
                if line[0:1] == "$" or line[0:1] == ";" or line[0:2] == "##":
                    continue
                try:
                    token = line.split("\t")[0]
                    tag = line.split("\t")[3]  # 2: pos, 3: ner
                    for i, syllable in enumerate(
                        token
                    ):  # 음절 단위로 잘라서 (형태소 단위 -> 음절 단위로 바꿔주기 위함)
                        tokens.append(syllable)  # 음절 단위 정보를 가져와서 문장을 만들어 감.
                        modi_tag = tag
                        if i > 0:
                            if tag[0] == "B":
                                modi_tag = (
                                    "I" + tag[1:]
                                )  # BIO tag를 부착할게요 :-) (잘라진 음절에 대해서도 BIO 태크를 붙이는 과정을 거치게 됨)
                        tags.append(modi_tag)
                except:
                    print(line)
            token_docs.append(tokens)
            tag_docs.append(tags)

    return token_docs, tag_docs


def encode_tags(tags, max_seq_length, tag2id):
    # label 역시 입력 token과 개수를 맞춰줍니다 :-) (truncation, padding 과정이 들어가야.. )
    tags = tags[: max_seq_length - 2]
    labels = [tag2id[tag] for tag in tags]
    labels = [tag2id["O"]] + labels

    padding_length = max_seq_length - len(labels)
    labels = labels + ([tag2id["O"]] * padding_length)

    return labels


def get_labels(train_tags, test_tags, tag2id):
    train_labels = []
    test_labels = []
    for tag in train_tags:
        train_labels.append(encode_tags(tag, 128, tag2id))
    for tag in test_tags:
        test_labels.append(encode_tags(tag, 128, tag2id))

    return train_labels, test_labels


def tokenized_sentences(train_texts, test_texts, tokenizer):

    tokenized_train_sentences = []
    tokenized_test_sentences = []
    for text in train_texts:  # 전체 데이터를 tokenizing 합니다.
        tokenized_train_sentences.append(ner_tokenizer(text, 128, tokenizer))
    for text in test_texts:
        tokenized_test_sentences.append(ner_tokenizer(text, 128, tokenizer))

    return tokenized_train_sentences, tokenized_test_sentences


def ner_tokenizer(
    sent, max_seq_length, tokenizer, pad_token_id=0, cls_token_id=101, sep_token_id=102
):

    pre_syllable = "_"
    input_ids = [pad_token_id] * (max_seq_length - 1)
    attention_mask = [0] * (max_seq_length - 1)
    token_type_ids = [0] * max_seq_length
    sent = sent[: max_seq_length - 2]

    for i, syllable in enumerate(sent):
        if syllable == "_":
            pre_syllable = syllable
        if pre_syllable != "_":
            syllable = "##" + syllable  # 중간 음절에는 모두 prefix를 붙입니다.
            # 이순신은 조선 -> [이, ##순, ##신, ##은, 조, ##선]
        pre_syllable = syllable

        input_ids[i] = tokenizer.convert_tokens_to_ids(syllable)
        attention_mask[i] = 1

    input_ids = [cls_token_id] + input_ids
    input_ids[len(sent) + 1] = sep_token_id
    attention_mask = [1] + attention_mask
    attention_mask[len(sent) + 1] = 1

    return {
        "input_ids": input_ids,  # 기존의 토크나이저가 반환하는 것과 동일한 형태로 반환함.
        "attention_mask": attention_mask,
        "token_type_ids": token_type_ids,
    }
