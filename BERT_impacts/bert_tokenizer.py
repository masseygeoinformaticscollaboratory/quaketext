# code adapted from the following tutorials
# Marmon, A. (2021). Fine-Tuned Named Entity Recognition with Hugging Face BERT. https://medium.com/@andrewmarmon/fine-tuned-named-entity-recognition-with-hugging-face-bert-d51d4cb3d7b5
# HuggingFace. (2020) Fine-tuning with custom datasets. https://huggingface.co/transformers/v3.2.0/custom_datasets.html#tok-ner

import os
import itertools
import pandas as pd
import numpy as np
from datasets import Dataset
from datasets import load_metric
from transformers import AutoTokenizer
from transformers import AutoModelForTokenClassification, TrainingArguments, Trainer, DistilBertForTokenClassification
from transformers import DataCollatorForTokenClassification
import torch

label_list = ['O','B-IMPACT','I-IMPACT','B-AFFECTED','I-AFFECTED','B-SEVERITY','I-SEVERITY','B-LOCATION','I-LOCATION','B-MODIFIER','I-MODIFIER']
label_encoding_dict = {
'O': 0, 
'B-IMPACT': 1, 
'I-IMPACT': 2, 
'B-AFFECTED': 3, 
'I-AFFECTED': 4, 
'B-SEVERITY': 5, 
'I-SEVERITY': 6, 
'B-LOCATION': 7, 
'I-LOCATION': 8, 
'B-MODIFIER': 9, 
'I-MODIFIER': 10}

unique_tags = set(label_list)
# tag2id = {tag: id for id, tag in enumerate(unique_tags)}
# id2tag = {id: tag for tag, id in tag2id.items()}
tag2id = label_encoding_dict
id2tag = {id: tag for tag, id in tag2id.items()}

task = "ner" 
model_checkpoint = "xlm-roberta-base" # try changing this to other this with auto tokeniser AND to one tag at a time need more dat files for that
batch_size = 16
    
# tokenizer = AutoTokenizer.from_pretrained(model_checkpoint)

# for roberta
tokenizer = AutoTokenizer.from_pretrained(model_checkpoint,add_prefix_space=True)


def get_all_tokens_and_ner_tags(directory):
    return pd.concat([get_tokens_and_ner_tags(os.path.join(directory, filename)) for filename in os.listdir(directory)]).reset_index().drop('index', axis=1)
    
def get_tokens_and_ner_tags(filename):
    with open(filename, 'r', encoding="utf8") as f:
        lines = f.readlines()
        split_list = [list(y) for x, y in itertools.groupby(lines, lambda z: z == '\n') if not x]
        tokens = [[x.split('\t')[0] for x in y] for y in split_list]
        entities = [[x.split('\t')[1][:-1] for x in y] for y in split_list] 
    return pd.DataFrame({'tokens': tokens, 'ner_tags': entities})
  
def get_un_token_dataset(train_directory, test_directory):
    train_df = get_all_tokens_and_ner_tags(train_directory)
    test_df = get_all_tokens_and_ner_tags(test_directory)
    train_dataset = Dataset.from_pandas(train_df)
    test_dataset = Dataset.from_pandas(test_df)

    return (train_dataset, test_dataset)

train_dataset, test_dataset = get_un_token_dataset('./tagged-training/', './tagged-test/')



def tokenize_and_align_labels(examples):
    label_all_tokens = True
    tokenized_inputs = tokenizer(list(examples["tokens"]), truncation=True, is_split_into_words=True)

    labels = []
    for i, label in enumerate(examples[f"{task}_tags"]):
        word_ids = tokenized_inputs.word_ids(batch_index=i)
        previous_word_idx = None
        label_ids = []
        for word_idx in word_ids:
            if word_idx is None:
                label_ids.append(-100)
            elif label[word_idx] == '0':
                label_ids.append(0)
            elif word_idx != previous_word_idx:
                label_ids.append(label_encoding_dict[label[word_idx]])
            else:
                label_ids.append(label_encoding_dict[label[word_idx]] if label_all_tokens else -100)
            previous_word_idx = word_idx
        labels.append(label_ids)
        
    tokenized_inputs["labels"] = labels
    return tokenized_inputs


train_tokenized_datasets = train_dataset.map(tokenize_and_align_labels, batched=True)
test_tokenized_datasets = test_dataset.map(tokenize_and_align_labels, batched=True)

model = AutoModelForTokenClassification.from_pretrained(model_checkpoint, num_labels=len(label_list), label2id=tag2id, id2label=id2tag)
# model = DistilBertForTokenClassification.from_pretrained(model_checkpoint, num_labels=len(label_list), label2id=tag2id, id2label=id2tag)

args = TrainingArguments(
    f"test-{task}",
    evaluation_strategy = "epoch",
    learning_rate=1e-4,
    per_device_train_batch_size=batch_size,
    per_device_eval_batch_size=batch_size,
    num_train_epochs=3,
    weight_decay=1e-5,
)

data_collator = DataCollatorForTokenClassification(tokenizer)
metric = load_metric("seqeval")


def compute_metrics(p):
    predictions, labels = p
    predictions = np.argmax(predictions, axis=2)

    true_predictions = [[label_list[p] for (p, l) in zip(prediction, label) if l != -100] for prediction, label in zip(predictions, labels)]
    true_labels = [[label_list[l] for (p, l) in zip(prediction, label) if l != -100] for prediction, label in zip(predictions, labels)]

    results = metric.compute(predictions=true_predictions, references=true_labels)
    return {"precision": results["overall_precision"], "recall": results["overall_recall"], "f1": results["overall_f1"], "accuracy": results["overall_accuracy"]}
    
trainer = Trainer(
    model,
    args,
    train_dataset=train_tokenized_datasets,
    eval_dataset=test_tokenized_datasets,
    data_collator=data_collator,
    tokenizer=tokenizer,
    compute_metrics=compute_metrics
)

trainer.train()
trainer.evaluate()

model_filename = model_checkpoint + "-ner.model"
trainer.save_model(model_filename)
