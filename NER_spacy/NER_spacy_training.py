import json
import spacy
from spacy import displacy
from spacy.util import minibatch, compounding, filter_spans
from spacy.training.example import Example
from spacy.tokens import DocBin
import random

training_data = []

# https://turbolab.in/build-a-custom-ner-model-using-spacy-3-0/ #VERY HELPFUL

def add_json_data_for_training(json_data):
    print("here")

    entity_tags = {'entities':[]}

    for i in json_data:
    # print(json_data[i]['content'])
        tweet_text = json_data[i]['content']
        for tag in json_data[i]['annotations']:
            # print(tag['tag'])

            # looking only at impact tags first
            if(tag['tag'] == 'type of impact'):
                entity_tags['entities'].append((tag['start'], tag['end'],"IMPACT"))

    
    # training_data.append((tweet_text,{"entities":[(0,9,"IMP")]}))
    training_data.append((tweet_text,entity_tags))
    entity_tags = {'entities':[]}


# ------------------------------------------------------------------------

nlp=spacy.load('en_core_web_sm')

ner=nlp.get_pipe('ner')

training_MT_file = open('../CSVtoJSONcode/finaltags.json')
json_MT_data = json.load(training_MT_file)

training_Lighttag_file = open('../CSVtoJSONcode/lighttag_finaltags.json')
json_Lighttag_data = json.load(training_Lighttag_file)

IMPACT_LABEL = "IMPACT"

entity_tags = {'entities':[]}

# add_json_data_for_training (json_MT_data)
# add_json_data_for_training (all_training_data, json_Lighttag_data)

mt_tag_count = 0

for i in json_MT_data:
    # print(json_data[i]['content'])
    tweet_text = json_MT_data[i]['content']
    for tag in json_MT_data[i]['annotations']:
        # print(tag['tag'])

        # looking only at impact tags first
        if(tag['tag'] == 'type of impact'):
            entity_tags['entities'].append((tag['start'], tag['end'],"IMPACT"))
        elif(tag['tag'] == 'item affected'):
            entity_tags['entities'].append((tag['start'], tag['end'],"AFFECTED"))
        elif(tag['tag'] == 'severity or quantity'):
            entity_tags['entities'].append((tag['start'], tag['end'],"SEVERITY"))  
        elif(tag['tag'] == 'place name'):
            entity_tags['entities'].append((tag['start'], tag['end'],"PLACE"))
        elif(tag['tag'] == 'location modifier'):
            entity_tags['entities'].append((tag['start'], tag['end'],"LOC MOD"))
        mt_tag_count += 1
    # training_data.append((tweet_text,{"entities":[(0,9,"IMP")]}))
    training_data.append((tweet_text,entity_tags))
    entity_tags = {'entities':[]}

print(len(training_data))
print("mt tag count",mt_tag_count)

light_tag_count = 0
imp_count = 0
aff_count = 0
sev_count = 0
place_count = 0
mod_count = 0

for i in json_Lighttag_data:
# print(json_data[i]['content'])
    tweet_text = json_Lighttag_data[i]['content']
    for tag in json_Lighttag_data[i]['annotations']:
        
        light_tag_count += 1 

        # looking only at impact tags first
        if(tag['tag'] == 'type of impact'):
            entity_tags['entities'].append((tag['start'], tag['end'],"IMPACT"))
            imp_count += 1
        elif(tag['tag'] == 'item affected'):
            entity_tags['entities'].append((tag['start'], tag['end'],"AFFECTED"))
            aff_count += 1
        elif(tag['tag'] == 'severity or quantity'):
            entity_tags['entities'].append((tag['start'], tag['end'],"SEVERITY"))  
            sev_count += 1
        elif(tag['tag'] == 'place name'):
            entity_tags['entities'].append((tag['start'], tag['end'],"PLACE"))
            place_count += 1
        elif(tag['tag'] == 'location modifier'):
            entity_tags['entities'].append((tag['start'], tag['end'],"LOC MOD"))
            mod_count += 1
        else:
            print(tag['tag'])
            print(tweet_text)
            print("here")
        
        
    # training_data.append((tweet_text,{"entities":[(0,9,"IMP")]}))
    training_data.append((tweet_text,entity_tags))
    entity_tags = {'entities':[]}

print("imp_count",imp_count)
print("aff_count",aff_count)
print("sev_count",sev_count)
print("place_count",place_count)
print("mod_count",mod_count)

print("total tag count from each",imp_count+aff_count+sev_count+mod_count+place_count)

print(len(training_data))
print("light tag count",light_tag_count)
print("total tag count",light_tag_count+mt_tag_count)


random.shuffle(training_data)
print ("--")
none_count = 0
none_type = {"IMPACT": 0, "AFFECTED" : 0, "SEVERITY" : 0, "PLACE": 0, "LOC MOD": 0}
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
            print(text[int(start):int(end)])
            none_type[label] += 1
            none_count += 1
        else:
            # ents_train.append(span)
            count += 1
            if(count < 4237): #20% = 4237 10% = 4767
                ents_train.append(span)
            else:
                ents_dev.append(span)
            
    # print(ents)
    ents_train_filtered = filter_spans(ents_train)
    ents_dev_filtered = filter_spans(ents_dev)

    doc_train.ents = ents_train_filtered
    db_train.add(doc_train)
    doc_dev.ents = ents_dev_filtered
    db_dev.add(doc_dev)


db_dev.to_disk("./dev.spacy")
db_train.to_disk("./train.spacy")
# db_train.to_disk("./dev.spacy")


print("count", count)
print("none_count", none_count)
print(none_type)


# TODO Run on more examples -  calculate scores of things 