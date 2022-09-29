import json
import spacy
from spacy import displacy

NER=spacy.load('en_core_web_sm')

training_file = open('../CSVtoJSONcode/finaltags.json')
json_data = json.load(training_file)

training_data = []

entity_tags = {'entities':[]}

for i in json_data:
    # print(json_data[i]['content'])
    tweet_text = json_data[i]['content']
    for tag in json_data[i]['annotations']:
        # print(tag['tag'])
        entity_tags['entities'].append((tag['start'], tag['end'],tag['tag']))
        
    
    # training_data.append((tweet_text,{"entities":[(0,9,"IMP")]}))
    training_data.append((tweet_text,entity_tags))
    entity_tags = {'entities':[]}
    
    # for anno in json_data[i]['annotations']:
        # if count < 10:
            # print(anno)
            # count = count+1

print(training_data)
# print(entity_tags)


raw_text="BREAKING: A 7.8-magnitude earthquake struck off Chile's northern coast Wednesday night, triggering a tsunami... http://t.co/WRbyO79to2"

text1= NER(raw_text)

for word in text1.ents:
    print(word.text,word.label_)