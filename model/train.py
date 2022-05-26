import os
import torch
import argparse
from sklearn.model_selection import train_test_split
from transformers.utils import logging
from transformers import AutoConfig, AutoTokenizer, AutoModelForTokenClassification, Trainer, TrainingArguments
from dataloader import load_file, read_file, tokenized_sentences, get_labels
from dataset import TokenDataset


def train(args):

    # txt 파일(개체명 인식 데이터)들을 불러오기
    file_list = load_file(args.data_path)
    # 파일 내용을 형태소 => 음절 단위로 읽어주기(text, tag 둘 다).
    texts, tags = read_file(file_list)

    # 음절 단위로 전처리 했을 때의 unique_tags와 tag와 id mapping
    unique_tags = set(tag for doc in tags for tag in doc)
    tag2id = {tag: id for id, tag in enumerate(unique_tags)}
    id2tag = {id: tag for tag, id in tag2id.items()}

    MODEL_NAME = args.model
    device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')

    model_config = AutoConfig.from_pretrained(MODEL_NAME)
    model_config.num_labels = len(unique_tags)

    model = AutoModelForTokenClassification.from_pretrained(MODEL_NAME, config=model_config)
    model.to(device)

    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

    # split
    train_texts, test_texts, train_tags, test_tags = train_test_split(texts, tags, test_size=0.2)
    
    # tokenizing sentence & getting label
    tokenized_train_sentences, tokenized_test_sentences = tokenized_sentences(train_texts, test_texts, tokenizer, MODEL_NAME)
    train_labels, test_labels = get_labels(train_tags, test_tags, tag2id)
    
    # make dataset
    train_dataset = TokenDataset(tokenized_train_sentences, train_labels)
    test_dataset = TokenDataset(tokenized_test_sentences, test_labels)

    print("Training Start")
    print("="*100)
    print(f"DEVICE : {device}")

    # training option
    training_args = TrainingArguments(
        output_dir=args.save_dir,  # output directory
        num_train_epochs=args.epochs,  # total number of training epochs
        per_device_train_batch_size=args.batch,  # batch size per device during training
        per_device_eval_batch_size=args.batch_valid,  # batch size for evaluation
        logging_dir="./logs",  # directory for storing logs
        logging_steps=args.logging_steps,
        learning_rate=args.lr,
        save_total_limit=5,
    )

    # trainer
    trainer = Trainer(
        model=model,  # the instantiated 🤗 Transformers model to be trained
        args=training_args,  # training arguments, defined above
        train_dataset=train_dataset,  # training dataset
        eval_dataset=test_dataset,  # evaluation dataset
    )

    trainer.train()
    path = os.path.join("./best_model", args.experiment_name)
    model.save_pretrained(path)


def main():

    parser = argparse.ArgumentParser()

    """path, model option"""
    parser.add_argument("--seed", type=int, default=42,
                        help="random seed (default: 42)")
    parser.add_argument("--model", type=str, default="klue/roberta-large",
                        help="model type (default: klue/bert-base)")
    parser.add_argument('--save_dir', type=str, default='./results',
                        help='model save dir path (default : ./results)')
    parser.add_argument('--data_path', type=str, default='/opt/ml/NER',
                        help='data path (default: /opt/ml/NER')
    parser.add_argument('--experiment_name', type=str, default= 'roberta_epoch1',
                        help='experiment name (default: test)')

    """hyperparameter"""
    parser.add_argument("--epochs", type=int, default=1,
                        help="number of epochs to train (default: 5)")
    parser.add_argument('--lr', type=float, default=5e-5,
                        help='learning rate (default: 5e-5)')
    parser.add_argument('--batch', type=int, default=16,
                        help='input batch size for training (default: 16)')
    parser.add_argument('--batch_valid', type=int, default=16,
                        help='input batch size for validing (default: 16)')
    parser.add_argument('--logging_steps', type=int,
                        default=100, help='logging_steps (default: 100)')

    args = parser.parse_args()

    logging.set_verbosity_warning()
    logger = logging.get_logger()
    logger.warning("\n")

    train(args)


if __name__ == '__main__':
    main()
