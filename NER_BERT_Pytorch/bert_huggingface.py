import csv

import re

from sklearn.model_selection import train_test_split
from transformers import DistilBertTokenizerFast
import numpy as np



with open("bio_tagged_data_MT.csv", 'r', encoding = 'utf-8') as MT_csv_file:

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

train_texts, val_texts, train_tags, val_tags = train_test_split(word_list, tag_list, test_size=.5)


unique_tags = set(tag for doc in tag_list for tag in doc)
tag2id = {tag: id for id, tag in enumerate(unique_tags)}
id2tag = {id: tag for tag, id in tag2id.items()}

print(tag2id)
print(id2tag)

tokenizer = DistilBertTokenizerFast.from_pretrained('distilbert-base-cased')
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

        # print()
        # print(doc_labels)
        # print(doc_enc_labels)
        # print(doc_offset)
        # print(arr_offset)

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