import sys
sys.path.append("model")
import torch
import numpy as np
from dataloader import ner_tokenizer
from utilities import *
from extract_info import *

def inference(text, model, tokenizer, device, finder, is_bert=False):  # 학습된 모델을 가지고 추론을 진행해보자.

    tag2id = load_tag2id()
    
    model.eval()
    text = text.replace(" ", "_")

    predictions, true_labels = [], []

    tokenized_sent = ner_tokenizer(text, len(text) + 2, tokenizer, is_bert)

    if is_bert:
        input_ids = (torch.tensor(tokenized_sent["input_ids"]).unsqueeze(0).to(device))
        attention_mask = (torch.tensor(tokenized_sent["attention_mask"]).unsqueeze(0).to(device))
        token_type_ids = (torch.tensor(tokenized_sent["token_type_ids"]).unsqueeze(0).to(device))
    else:
        input_ids = (torch.tensor(tokenized_sent["input_ids"]).unsqueeze(0).to(device))
        attention_mask = (torch.tensor(tokenized_sent["attention_mask"]).unsqueeze(0).to(device))

    with torch.no_grad():
        if is_bert:
            outputs = model(
                input_ids=input_ids,
                attention_mask=attention_mask,
                token_type_ids=token_type_ids,
            )
        else:
            outputs = model(
            input_ids=input_ids,
            attention_mask=attention_mask
        )

    logits = outputs["logits"]
    logits = logits.detach().cpu().numpy()
    
    if is_bert:
        label_ids = token_type_ids.cpu().numpy()
        true_labels.append(label_ids)

    predictions.extend([list(p) for p in np.argmax(logits, axis=2)])
    

    pred_tags = [list(tag2id.keys())[p_i] for p in predictions for p_i in p]
    
    texts = []
    tags = []
    for i, tag in enumerate(pred_tags):
        texts.append(tokenizer.convert_ids_to_tokens(tokenized_sent["input_ids"][i]))
        tags.append(tag)

    return texts, tags

def inf_main(text, model, tokenizer, device, finder):
    texts, tags = inference(text, model, tokenizer, device, finder)
    ret = extract_info(texts, tags, finder)
    return ret