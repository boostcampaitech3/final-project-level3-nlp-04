import os
import sys
sys.path.append("./model")
import torch
import argparse
import numpy as np
from sklearn.model_selection import train_test_split
from transformers import AutoTokenizer, AutoModelForTokenClassification
from dataloader import ner_tokenizer
from utilities import *
from extract_info import *


def inference(args, text):  # 학습된 모델을 가지고 추론을 진행해보자.

    tag2id = load_tag2id()
    
    device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
    # load tokenizer

    # 주의. 저장된 모델과 동일한 토크나이저를 사용하여 한다.
    Tokenizer_NAME = args.model
    tokenizer = AutoTokenizer.from_pretrained(Tokenizer_NAME)

    ## load my model
    MODEL_NAME = os.path.join(args.model_dir, args.model_name) # model dir.
    model = AutoModelForTokenClassification.from_pretrained(MODEL_NAME)
    model.parameters
    model.to(device)

    model.eval()
    text = text.replace(" ", "_")

    predictions, true_labels = [], []

    tokenized_sent = ner_tokenizer(text, len(text) + 2, tokenizer, Tokenizer_NAME)

    if args.model == 'klue/roberta-large':
        input_ids = (torch.tensor(tokenized_sent["input_ids"]).unsqueeze(0).to(device))
        attention_mask = (torch.tensor(tokenized_sent["attention_mask"]).unsqueeze(0).to(device))
    else:
        input_ids = (torch.tensor(tokenized_sent["input_ids"]).unsqueeze(0).to(device))
        attention_mask = (torch.tensor(tokenized_sent["attention_mask"]).unsqueeze(0).to(device))
        token_type_ids = (torch.tensor(tokenized_sent["token_type_ids"]).unsqueeze(0).to(device))

    with torch.no_grad():
        if args.model == 'klue/roberta-large':
            outputs = model(
            input_ids=input_ids,
            attention_mask=attention_mask
        )
        else:
            outputs = model(
                input_ids=input_ids,
                attention_mask=attention_mask,
                token_type_ids=token_type_ids,
            )

    logits = outputs["logits"]
    logits = logits.detach().cpu().numpy()
    
    if args.model != 'klue/roberta-large':
        label_ids = token_type_ids.cpu().numpy()
        true_labels.append(label_ids)

    predictions.extend([list(p) for p in np.argmax(logits, axis=2)])
    

    pred_tags = [list(tag2id.keys())[p_i] for p in predictions for p_i in p]

    print("{}\t{}".format("TOKEN", "TAG"))
    print("===========")
    
    texts = []
    tags = []
    for i, tag in enumerate(pred_tags):
        texts.append(tokenizer.convert_ids_to_tokens(tokenized_sent["input_ids"][i]))
        tags.append(tag)
        print("{:^5}\t{:^5}".format(tokenizer.convert_ids_to_tokens(tokenized_sent["input_ids"][i]), tag,))

    return texts, tags


def inf_main(text):

    parser = argparse.ArgumentParser()
    
    '''path, model option & dir'''
    parser.add_argument("--model", type=str, default="klue/roberta-large")
    parser.add_argument('--data_path', type=str, default='/opt/ml/NER')
    parser.add_argument('--model_dir', type=str, default="./model/best_model")
    parser.add_argument('--model_name', type=str, default="bert_final_roberta")

    args = parser.parse_args()

    print(args)
    
    # text = "차투차 CHATOCHA 금융부분이사 본사 경기도 수원시 권선구 세화로 44 (평동) 박원주 수원지점 경기도 수원시 권선구 권선로 308-5 도이치월드 219호"
    texts, tags = inference(args, text)
    return extract_info(texts, tags)
    
if __name__ == '__main__':
    inf_main()