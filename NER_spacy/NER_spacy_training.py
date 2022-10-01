# from __future__ import annotations
import json
import spacy
from spacy import displacy
from spacy.util import minibatch, compounding
from spacy.training.example import Example
from spacy.tokens import DocBin
import random

# https://turbolab.in/build-a-custom-ner-model-using-spacy-3-0/ #VERY HELPFUL

nlp=spacy.load('en_core_web_sm')

ner=nlp.get_pipe('ner')

training_file = open('../CSVtoJSONcode/finaltags.json')
json_data = json.load(training_file)

IMPACT_LABEL = "IMPACT"

training_data = []

entity_tags = {'entities':[]}

for i in json_data:
    # print(json_data[i]['content'])
    tweet_text = json_data[i]['content']
    for tag in json_data[i]['annotations']:
        # print(tag['tag'])

        # looking only at impact tags first
        if(tag['tag'] == 'type of impact'):
            entity_tags['entities'].append((tag['start'], tag['end'],"IMPACT"))
            if(tag['value'] == "Riots"):
                print(tag['value'])
            
        
    
    # training_data.append((tweet_text,{"entities":[(0,9,"IMP")]}))
    training_data.append((tweet_text,entity_tags))
    entity_tags = {'entities':[]}
    
    # for anno in json_data[i]['annotations']:
        # if count < 10:
            # print(anno)
            # count = count+1

# print(training_data)
# print(entity_tags)

# ner.add_label(IMPACT_LABEL)

# optimizer = nlp.resume_training()
# move_names = list(ner.move_names)

# pipe_exceptions = ["ner", "trf_wordpiecer", "trf_tok2vec"]

# other_pipes = [pipe for pipe in nlp.pipe_names if pipe not in pipe_exceptions]

# with nlp.disable_pipes(*other_pipes):
#     sizes = compounding(1.0, 4.0, 1.001)
#     for itn in range(114):
#         random.shuffle(training_data)
#         batches = minibatch(training_data, size = sizes)
#         losses = {}
#         for batch in batches:
#             texts, annotations = zip(*batch)
#             # nlp.update(texts, annotations, sgd=optimizer, drop=0.35, losses=losses)
#             # print("losses", losses)
#             for text, annotations in batch:
#                 print(annotations)
#                 print(text)
#                 doc = nlp.make_doc(text)
#                 example = Example.from_dict(doc, annotations)
#                 nlp.update([example], losses=losses, drop=0.35)
#             print("losses",losses)
print ("--")
none_count = 0
count = 0
nlp = spacy.blank("en")
# training_data = [
#   ("Tokyo Tower is 333m tall.", [(0, 11, "BUILDING")]),
# ]
# the DocBin will store the example documents
db_train = DocBin()
db_dev = DocBin()
for text, annotations in training_data:
    
    # print(annotations)
    # print(text)
    doc_train = nlp(text)
    doc_dev = nlp(text)
    ents_train = []
    ents_dev = []
    for start, end, label in annotations['entities']:
        
        span = doc_train.char_span(int(start), int(end), label=label)
        # print(span)
        if str(span) == "None":
            # TODO issue here with tokenizing words without spaces between them
            print(text)
            print(label)
            print(start)
            print(end)
            none_count += 1
        else:
            count += 1
            if(count < 500):
                ents_train.append(span)
            else:
                ents_dev.append(span)
            
    # print(ents)
    

    doc_train.ents = ents_train
    db_train.add(doc_train)
    doc_dev.ents = ents_dev
    db_dev.add(doc_dev)


db_dev.to_disk("./dev.spacy")
db_train.to_disk("./train.spacy")

print("count", count)
print("none_count", none_count)


raw_text="BREAKING: A 7.8-magnitude earthquake struck off Chile's northern coast Wednesday night, triggering a tsunami... http://t.co/WRbyO79to2"

doc = nlp(raw_text)
print("Entities in '%s'" % raw_text)
for ent in doc.ents:
    print(ent)

# text1= NER(raw_text)

# for word in text1.ents:
#     print(word.text,word.label_)