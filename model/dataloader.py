import re
import os
import glob
from pathlib import Path

'''dataloader 단에서 필요한 것?'''
# TODO: load_file(file_path) : txt 파일 데이터 불러오기
# TODO: read_file(file_list) : 여러 파일의 데이터 전처리하기
    #   1) pickle 파일로 미리 저장한 것을 빠르게 불러오기
# TODO: tokenized_sentences(text, tokenizer) : text를 토큰화하기
    # TODO: ner_tokenzier(text, max_seq_lenght, tokenizer) 
    #   1) text 토큰화를 할 때, 음절 단위로 토큰화하기
    #   2) 출력값으로 다양한 모델에 맞춰 줄 수 있도록 하기                                            
# TODO: get_label(text, ... ) : 각 tag에 맞는 label 값 지정하기
    # TODO: encode_tag(tag, max_seq_length, tag2id) : text로 되어 있는 tag들을 id 값으로 바꿔주기

def load_file(file_path):
    file_list = []
    for x in os.walk(file_path):
        for y in glob.glob(os.path.join(x[0], "*_NER.txt")):  # ner.*, *_NER.txt
            file_list.append(y)

    return file_list


def read_file(file_list):

    token_docs = []
    tag_docs = []
    for file_path in file_list:
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
                    for i, syllable in enumerate(token):  # 음절 단위로 잘라서 (형태소 단위 -> 음절 단위로 바꿔주기 위함)
                        tokens.append(syllable)  # 음절 단위 정보를 가져와서 문장을 만들어 감.
                        modi_tag = tag
                        if i > 0:
                            if tag[0] == "B":
                                modi_tag = "I" + tag[1:] # 잘라진 음절에 대해서도 BIO 태크를 붙이는 과정을 거치게 됨
                                                        # 음절 단위로 잘라지면서, 첫 글자를 제외한 부분은 I-** 형태로 들어감.
                        tags.append(modi_tag)
                except:
                    print(line)
            token_docs.append(tokens)
            tag_docs.append(tags)
    
    return token_docs, tag_docs



# def load_data(file_path):

#     if os.path.isfile(f'token.pkl') and os.path.isfile(f'tag.pkl'):
#         return load_preprocessed_data()
#     # txt 파일(개체명 인식 데이터)들을 불러오기
#     file_list = load_file(file_path)
#     # 파일 내용을 형태소 => 음절 단위로 읽어주기(text, tag 둘 다).
#     texts, tags = read_file(file_list)

#     return texts, tags


def ner_tokenizer(sent, max_seq_length, tokenizer, MODEL_NAME):  

    pad_token_id = tokenizer.pad_token_id # 0 
    cls_token_id = tokenizer.cls_token_id # 101
    sep_token_id = tokenizer.sep_token_id # 102

    pre_syllable = "_"

    # tokenizer 결과값을 담을 공간 만들기
    input_ids = [pad_token_id] * (max_seq_length - 1)
    attention_mask = [0] * (max_seq_length - 1)
    token_type_ids = [0] * max_seq_length
    
    # 문장 앞 뒤로 CLS, SEP 값을 넣어줘야 함. 최대 길이를 기준으로 2자리만 비워둠.
    sent = sent[:max_seq_length-2]

    for i, syllable in enumerate(sent):
        if syllable == '_':
            pre_syllable = syllable
        if pre_syllable != "_":
            syllable = '##' + syllable  # 중간 음절에는 모두 prefix를 붙입니다.
            # 이순신은 조선 -> [이, ##순, ##신, ##은, 조, ##선]
        pre_syllable = syllable

        # 음절 단위로 tokenize를 진행함
        input_ids[i] = (tokenizer.convert_tokens_to_ids(syllable))
        attention_mask[i] = 1
    
    # input_id
    input_ids = [cls_token_id] + input_ids
    input_ids[len(sent)+1] = sep_token_id

    # attention_mask
    attention_mask = [1] + attention_mask
    attention_mask[len(sent)+1] = 1

    # token_type_ids => QA task가 아니므로 모두 같은 값으로 넣어줌

    if MODEL_NAME == 'klue/roberta-large':
        return {"input_ids":input_ids, 
                "attention_mask":attention_mask}

    return {"input_ids":input_ids, 
            "attention_mask":attention_mask,
            "token_type_ids":token_type_ids}


def tokenized_sentences(train_texts, test_texts, tokenizer, MODEL_NAME):

    tokenized_train_sentences = []
    tokenized_test_sentences = []
    for text in train_texts:  # 전체 데이터를 tokenizing 합니다.
        tokenized_train_sentences.append(ner_tokenizer(text, 128, tokenizer, MODEL_NAME))
    for text in test_texts:
        tokenized_test_sentences.append(ner_tokenizer(text, 128, tokenizer, MODEL_NAME))

    return tokenized_train_sentences, tokenized_test_sentences


def get_labels(train_tags, test_tags, tag2id):
    train_labels = []
    test_labels = []
    for tag in train_tags:
        train_labels.append(encode_tags(tag, 128, tag2id))
    for tag in test_tags:
        test_labels.append(encode_tags(tag, 128, tag2id))

    return train_labels, test_labels


def encode_tags(tags, max_seq_length, tag2id):
    # label 역시 입력 token과 개수를 맞춰줍니다 :-) (truncation, padding 과정이 들어가야.. )
    tags = tags[: max_seq_length - 2]
    labels = [tag2id[tag] for tag in tags]
    labels = [tag2id["O"]] + labels

    padding_length = max_seq_length - len(labels)
    labels = labels + ([tag2id["O"]] * padding_length)

    return labels