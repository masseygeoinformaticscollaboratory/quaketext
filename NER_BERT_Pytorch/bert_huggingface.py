import csv

import re

from sklearn.model_selection import train_test_split
from transformers import DistilBertTokenizerFast
from transformers import Trainer, TrainingArguments, DistilBertForTokenClassification, EarlyStoppingCallback
import numpy as np
import transformers
from seqeval.metrics import classification_report, f1_score, precision_score, recall_score, accuracy_score


import torch

# print(torch.cuda.is_available())

# a=torch.cuda.FloatTensor()
# print(a)

# print(torch.__version__)

with open("bio_tagged_data_MT.csv", 'r', encoding = 'utf-8') as MT_csv_file:
# with open("wnut17train.csv", 'r', encoding = 'utf-8') as MT_csv_file:

    MT_csv_reader = csv.DictReader(MT_csv_file, delimiter='\t')

    # bio_file_path = Path("bio_tagged_data_MT.csv")

    # raw_text = bio_file_path.read_text().strip()
# raw_docs = re.split(r'\n\t?\n', raw_text)
    word_list = []
    tag_list = []
    tokens = []
    tags = []

    for row in MT_csv_reader:
        # print(row)
        

        token = row['word']
        tag = row['tag']
        tokens.append(token)
        tags.append(tag)

        word_list.append(tokens)
        tag_list.append(tags)

    # print(word_list)
    # print(tag_list)

print(word_list[0][0:17], tag_list[0][0:17], sep='\n')

train_texts, val_texts, train_tags, val_tags = train_test_split(word_list, tag_list, test_size=.2)


unique_tags = set(tag for doc in tag_list for tag in doc)
tag2id = {tag: id for id, tag in enumerate(unique_tags)}
id2tag = {id: tag for tag, id in tag2id.items()}

print(tag2id)
print(id2tag)


# class WNUTDatasetBatchLoader(torch.utils.data.Dataset):
#     def __init__(self, texts, tags, tokenizer):
#         self.texts = np.asanyarray(texts, dtype=list)
#         self.tags = np.asanyarray(tags, dtype=list)
#         self.tokenizer = tokenizer
        
#     def __len__(self):
#         return len(self.texts)
        
#     def __getitem__(self, idx):
#         if torch.is_tensor(idx):
#             idx = idx.tolist()
        
#         encodings = self.tokenizer(self.texts[idx],
#                               is_split_into_words=True,
#                               max_length=64,
#                               padding='max_length',
#                               truncation=True)
#         tags = self.tags[idx]
#         labels = align_labels(tags, encodings)
        
#         item = dict()
#         item['input_ids'] = torch.tensor(encodings.input_ids)
#         item['attention_mask'] = torch.tensor(encodings.attention_mask)
#         item['labels'] = torch.tensor(labels)            
        
#         return item
      
# def align_labels(tags: list, encodings: transformers.tokenization_utils_base.BatchEncoding, label_all_tokens=True) -> list:
#     labels = []
#     word_ids = encodings.word_ids()
#     prev_word_idx = None
#     label_ids = []
#     for word_idx in word_ids:
#         if word_idx is None:
#             label_ids.append(-100)
#         elif word_idx != prev_word_idx:
#             label_ids.append(tag2id[tags[word_idx]])
#         else:
#             label_ids.append(tag2id[tags[word_idx]] if label_all_tokens else -100)
#     return label_ids


  

# tokenizer = DistilBertTokenizerFast.from_pretrained('distilbert-base-cased')

# print("pre train encoding")
# train_dataset = WNUTDatasetBatchLoader(train_texts, train_tags, tokenizer)
# print("pre val encoding")
# val_dataset = WNUTDatasetBatchLoader(val_texts, val_tags, tokenizer)
# print("post val encoding")

# def compute_metrics(eval_predictions):
#     predictions, labels = eval_predictions.predictions, eval_predictions.label_ids
#     predictions = np.argmax(predictions, axis=2)

#     # Remove ignored index (special tokens)
#     true_predictions = [
#         [id2tag[p] for (p, l) in zip(prediction, label) if l != -100]
#         for prediction, label in zip(predictions, labels)
#     ]
#     true_labels = [
#         [id2tag[l] for (p, l) in zip(prediction, label) if l != -100]
#         for prediction, label in zip(predictions, labels)
#     ]
    
#     score_f1 = f1_score(true_labels, true_predictions)
#     score_prec = precision_score(true_labels, true_predictions)
#     score_rec = recall_score(true_labels, true_predictions)
#     score_acc = accuracy_score(true_labels, true_predictions)
    
#     return {
#         "precision": score_prec,
#         "recall": score_rec,
#         "f1": score_f1,
#         "accuracy": score_acc,
#     }


# model = DistilBertForTokenClassification.from_pretrained('distilbert-base-cased', num_labels=len(unique_tags))
# cb_early_stop = EarlyStoppingCallback(early_stopping_patience=3, early_stopping_threshold=1e-3)

# training_args = TrainingArguments(
#     output_dir='./results',          # output directory
#     overwrite_output_dir = True,
#     num_train_epochs=3,              # total number of training epochs
#     per_device_train_batch_size=16,  # batch size per device during training
#     per_device_eval_batch_size=64,   # batch size for evaluation
#     warmup_steps=500,                # number of warmup steps for learning rate scheduler
#     weight_decay=0.01,               # strength of weight decay
#     logging_dir='./logs',            # directory for storing logs
#     logging_steps=100,
#     load_best_model_at_end = True,
#     evaluation_strategy='steps',
#     save_total_limit=3,
# )

# trainer = Trainer(
#     model=model,                         # the instantiated 🤗 Transformers model to be trained
#     args=training_args,                  # training arguments, defined above
#     train_dataset=train_dataset,         # training dataset
#     eval_dataset=val_dataset,            # evaluation dataset
#     # compute_metrics=compute_metrics
# )

# trainer.add_callback(cb_early_stop)

# trainer.train()

# self.texts[idx],
#                               is_split_into_words=True,
#                               max_length=64,
#                               padding='max_length',
#                               truncation=True)

tokenizer = DistilBertTokenizerFast.from_pretrained('distilbert-base-cased', low_cpu_mem_usage=True)

print("pre train encoding")
train_encodings = tokenizer(train_texts, is_split_into_words=True, return_offsets_mapping=True, padding=True, truncation=True)
print("post train encoding")
print("pre val encoding")
val_encodings = tokenizer(val_texts, is_split_into_words=True, return_offsets_mapping=True, padding=True, truncation=True)
print("post val encoding")

def encode_tags(tags, encodings):
    labels = [[tag2id[tag] for tag in doc] for doc in tags]
    print("encode tags")
    encoded_labels = []
    for doc_labels, doc_offset in zip(labels, encodings.offset_mapping):
        # create an empty array of -100
        doc_enc_labels = np.ones(len(doc_offset),dtype=int) * -100
        arr_offset = np.array(doc_offset)

        print()
        print(doc_labels)
        print(doc_enc_labels)
        print(doc_offset)
        print(arr_offset)

        # if((arr_offset[:,0] == 0) & (arr_offset[:,1] != 0)):
        #     doc_enc_labels = doc_labels
        # set labels whose first offset position is 0 and the second is not 0
        doc_enc_labels[(arr_offset[:,0] == 0) & (arr_offset[:,1] != 0)] = doc_labels
        encoded_labels.append(doc_enc_labels.tolist())

    return encoded_labels


# print(train_tags)
# print(train_encodings)
train_labels = encode_tags(train_tags, train_encodings)
val_labels = encode_tags(val_tags, val_encodings)