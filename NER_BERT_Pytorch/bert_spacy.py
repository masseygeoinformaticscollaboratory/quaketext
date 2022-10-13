import json
import spacy
from spacy import displacy
from spacy.util import minibatch, compounding, filter_spans
from spacy.training.example import Example
from spacy.tokens import DocBin
import random
import re

IOB_data = []

impact_dict = {"type of impact": "IMPACT", "item affected" : "AFFECTED", "severity or quantity" : "SEVERITY", "place name": "LOCATION", "location modifier": "MODIFIER"}

# nlp=spacy.load('en_core_web_sm')

# ner=nlp.get_pipe('ner')

training_MT_file = open('../CSVtoJSONcode/finaltags.json')
json_MT_data = json.load(training_MT_file)

# train_bio_file = open("train_bio_tagged_data_MT.tsv", 'w', encoding = 'utf-8')
# dev_bio_file = open("dev_bio_tagged_data_MT.tsv", 'w', encoding = 'utf-8')

bio_file = open("bio_tagged_data_MT.csv", 'w', encoding = 'utf-8')
bio_file.write("word" + "\t" + "tag" + "\n")


# training_Lighttag_file = open('../CSVtoJSONcode/lighttag_finaltags.json')
# json_Lighttag_data = json.load(training_Lighttag_file)

mt_tag_count = 0
bio_tag = ""
foundTag = False
lastVal = ""
tweet_count = 0

for i in json_MT_data:
    # print(json_data[i]['content'])
    
    
    tweet_text = json_MT_data[i]['content']

    for word in re.split('\s|, |: |- |"',tweet_text):
        # print(word)
        for tag in json_MT_data[i]['annotations']:
            # print(tag['tag'])
            

            if word in tag['value'] and word != "":
                if(lastVal == tag['value']):
                    pre = "I-"
                else:
                    pre = "B-"

                lastVal = tag['value']
                bio_tag = pre + impact_dict[tag['tag']]
                foundTag = True
                mt_tag_count += 1
                

        if foundTag == False:
            bio_tag = "O"

        foundTag = False
        if word != "":

            bio_file.write(word + "\t" + bio_tag + "\n")
            # if tweet_count < 1000:
            #     train_bio_file.write(word + "\t" + bio_tag + "\n")
            # else:
            #     dev_bio_file.write(word + "\t" + bio_tag + "\n")
    
    tweet_count += 1

print(tweet_count)
print(mt_tag_count)

    # # training_data.append((tweet_text,{"entities":[(0,9,"IMP")]}))
    # training_data.append((tweet_text,entity_tags))
    # entity_tags = {'entities':[]}

# print(len(training_data))
# print("mt tag count",mt_tag_count)

# light_tag_count = 0
# imp_count = 0
# aff_count = 0
# sev_count = 0
# place_count = 0
# mod_count = 0

# for i in json_Lighttag_data:
# # print(json_data[i]['content'])
#     tweet_text = json_Lighttag_data[i]['content']
#     for tag in json_Lighttag_data[i]['annotations']:
        
#         light_tag_count += 1 

#         # looking only at impact tags first
#         if(tag['tag'] == 'type of impact'):
#             entity_tags['entities'].append((tag['start'], tag['end'],"IMPACT"))
#             imp_count += 1
#         elif(tag['tag'] == 'item affected'):
#             entity_tags['entities'].append((tag['start'], tag['end'],"AFFECTED"))
#             aff_count += 1
#         elif(tag['tag'] == 'severity or quantity'):
#             entity_tags['entities'].append((tag['start'], tag['end'],"SEVERITY"))  
#             sev_count += 1
#         elif(tag['tag'] == 'place name'):
#             entity_tags['entities'].append((tag['start'], tag['end'],"PLACE"))
#             place_count += 1
#         elif(tag['tag'] == 'location modifier'):
#             entity_tags['entities'].append((tag['start'], tag['end'],"LOC MOD"))
#             mod_count += 1
#         else:
#             print(tag['tag'])
#             print(tweet_text)
#             print("here")
        
        
#     # training_data.append((tweet_text,{"entities":[(0,9,"IMP")]}))
#     training_data.append((tweet_text,entity_tags))
#     entity_tags = {'entities':[]}

# print("imp_count",imp_count)
# print("aff_count",aff_count)
# print("sev_count",sev_count)
# print("place_count",place_count)
# print("mod_count",mod_count)

# print("total tag count from each",imp_count+aff_count+sev_count+mod_count+place_count)

# print(len(training_data))
# print("light tag count",light_tag_count)
# print("total tag count",light_tag_count+mt_tag_count)


# random.shuffle(training_data)
# print ("--")
# none_count = 0
# count = 0
# nlp = spacy.blank("en")
# # training_data = [
# #   ("Tokyo Tower is 333m tall.", [(0, 11, "BUILDING")]),
# # ]
# # the DocBin will store the example documents
# db_train = DocBin()
# db_dev = DocBin()
# for text, annotations in training_data:
    
#     # print(annotations)
#     # print(text)
#     doc_train = nlp(text)
#     doc_dev = nlp(text)
#     ents_train = []
#     ents_dev = []
#     for start, end, label in annotations['entities']:
        
#         span = doc_train.char_span(int(start), int(end), label=label)
#         # print(span)
#         if str(span) == "None":
#             # TODO issue here with tokenizing words without spaces between them
#             # print(text)
#             # print(label)
#             # print(start)
#             # print(end)
#             none_count += 1
#         else:
#             # ents_train.append(span)
#             count += 1
#             if(count < 4700):
#                 ents_train.append(span)
#             else:
#                 ents_dev.append(span)
            
#     # print(ents)
#     ents_train_filtered = filter_spans(ents_train)
#     ents_dev_filtered = filter_spans(ents_dev)

#     doc_train.ents = ents_train_filtered
#     db_train.add(doc_train)
#     doc_dev.ents = ents_dev_filtered
#     db_dev.add(doc_dev)


# db_dev.to_disk("./dev.spacy")
# db_train.to_disk("./train.spacy")
# # db_train.to_disk("./dev.spacy")


# print("count", count)
# print("none_count", none_count)


# # TODO Run on more examples -  calculate scores of things 