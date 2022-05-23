import torch
import numpy as np
from sklearn.model_selection import train_test_split
from transformers import (
    AutoTokenizer,
    BertForTokenClassification,
    Trainer,
    TrainingArguments,
)

from utilities import (
    load_file,
    read_file,
    get_labels,
    tokenized_sentences,
    ner_tokenizer,
)
from dataset import TokenDataset


class NER:
    def __init__(self):
        self.file_list = load_file()
        self.texts, self.tags = read_file(self.file_list[:])

        self.unique_tags = set(tag for doc in self.tags for tag in doc)
        self.tag2id = {tag: id for id, tag in enumerate(self.unique_tags)}
        self.id2tag = {id: tag for tag, id in self.tag2id.items()}

        MODEL_NAME = "klue/bert-base"

        self.model = BertForTokenClassification.from_pretrained(
            MODEL_NAME, num_labels=len(self.unique_tags)
        )
        self.tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
        self.device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

    def train(self):

        self.model.to(self.device)

        train_texts, test_texts, train_tags, test_tags = train_test_split(
            self.texts, self.tags, test_size=0.2
        )

        tokenized_train_sentences, tokenized_test_sentences = tokenized_sentences(
            train_texts, test_texts, self.tokenizer
        )
        train_labels, test_labels = get_labels(train_tags, test_tags, self.tag2id)

        train_dataset = TokenDataset(tokenized_train_sentences, train_labels)
        test_dataset = TokenDataset(tokenized_test_sentences, test_labels)

        training_args = TrainingArguments(
            output_dir="./results",  # output directory
            num_train_epochs=5,  # total number of training epochs
            per_device_train_batch_size=8,  # batch size per device during training
            per_device_eval_batch_size=64,  # batch size for evaluation
            logging_dir="./logs",  # directory for storing logs
            logging_steps=100,
            learning_rate=3e-5,
            save_total_limit=5,
        )

        trainer = Trainer(
            model=self.model,  # the instantiated 🤗 Transformers model to be trained
            args=training_args,  # training arguments, defined above
            train_dataset=train_dataset,  # training dataset
            eval_dataset=test_dataset,  # evaluation dataset
        )

        trainer.train()

    def inference(self, text):  # 학습된 모델을 가지고 추론을 진행해보자.

        self.model.eval()
        text = text.replace(" ", "_")

        predictions, true_labels = [], []

        tokenized_sent = ner_tokenizer(text, len(text) + 2, self.tokenizer)
        input_ids = (
            torch.tensor(tokenized_sent["input_ids"]).unsqueeze(0).to(self.device)
        )
        attention_mask = (
            torch.tensor(tokenized_sent["attention_mask"]).unsqueeze(0).to(self.device)
        )
        token_type_ids = (
            torch.tensor(tokenized_sent["token_type_ids"]).unsqueeze(0).to(self.device)
        )

        with torch.no_grad():
            outputs = self.model(
                input_ids=input_ids,
                attention_mask=attention_mask,
                token_type_ids=token_type_ids,
            )

        logits = outputs["logits"]
        logits = logits.detach().cpu().numpy()
        label_ids = token_type_ids.cpu().numpy()

        predictions.extend([list(p) for p in np.argmax(logits, axis=2)])
        true_labels.append(label_ids)

        pred_tags = [list(self.tag2id.keys())[p_i] for p in predictions for p_i in p]

        print("{}\t{}".format("TOKEN", "TAG"))
        print("===========")
        # for token, tag in zip(tokenizer.decode(tokenized_sent['input_ids']), pred_tags):
        #   print("{:^5}\t{:^5}".format(token, tag))
        for i, tag in enumerate(pred_tags):
            print(
                "{:^5}\t{:^5}".format(
                    self.tokenizer.convert_ids_to_tokens(
                        tokenized_sent["input_ids"][i]
                    ),
                    tag,
                )
            )


if __name__ == "__main__":
    ner = NER()
    ner.train()
    ner.inference("금융부분이사  박원주")
