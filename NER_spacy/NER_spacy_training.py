# code adapted from the following tutorials
# Spacy. Training Pipelines & Models. https://spacy.io/usage/training
# Turbolab. Build a Custom NER model using spaCy 3.0. https://turbolab.in/build-a-custom-ner-model-using-spacy-3-0/
import json
import spacy
from spacy import displacy
from spacy.util import minibatch, compounding, filter_spans
from spacy.tokens import DocBin
import random

training_data = []
validation_data = []

TEN_FOLD_ROUND_NUM = 0 # 0-9 depending on round

nlp=spacy.load('en_core_web_sm')
ner=nlp.get_pipe('ner')

# Mechanical turk data
training_MT_file = open('../CSVtoJSONcode/finaltags.json')
json_MT_data = json.load(training_MT_file)

print("len(json_MT_data)",len(json_MT_data))
total_MT_tweets = len(json_MT_data)

# Light Tag data
training_Lighttag_file = open('../CSVtoJSONcode/lighttag_finaltags.json')
json_Lighttag_data = json.load(training_Lighttag_file)

print("len(json_Lighttag_data)",len(json_Lighttag_data))
total_LightTag_tweets = len(json_Lighttag_data)

entity_tags = {'entities':[]}

mt_tag_count = 0
tweet_count = 0

# loop through each tweet dictionary item
for i in json_MT_data:

    tweet_text = json_MT_data[i]['content']
    
    for tag in json_MT_data[i]['annotations']:

        # for each tag in the list of annotations add to entity tag dictionary containing a list of entities 
        if(tag['tag'] == 'type of impact'):
            entity_tags['entities'].append((tag['start'], tag['end'],"IMPACT"))
        elif(tag['tag'] == 'item affected'):
            entity_tags['entities'].append((tag['start'], tag['end'],"AFFECTED"))
        elif(tag['tag'] == 'severity or quantity'):
            entity_tags['entities'].append((tag['start'], tag['end'],"SEVERITY"))  
        elif(tag['tag'] == 'place name'):
            entity_tags['entities'].append((tag['start'], tag['end'],"LOCATION"))
        elif(tag['tag'] == 'location modifier'):
            entity_tags['entities'].append((tag['start'], tag['end'],"MODIFIER"))
        mt_tag_count += 1
    

    # determine the tweets that are validation or training
    if(tweet_count > (total_MT_tweets/10) * TEN_FOLD_ROUND_NUM) and (tweet_count < (total_MT_tweets/10) * (TEN_FOLD_ROUND_NUM + 1)):
        validation_data.append((tweet_text,entity_tags))
        print((tweet_text,entity_tags))
    else:
        training_data.append((tweet_text,entity_tags))

    entity_tags = {'entities':[]}
    tweet_count+=1

print("tweet count", tweet_count)
print("t, v",len(training_data), len(validation_data))
print("total",len(training_data) + len(validation_data))
print("mt tag count",mt_tag_count)
print()

light_tag_count = 0
tweet_count = 0

# append the light tag data onto the entity tags
for i in json_Lighttag_data:

    tweet_text = json_Lighttag_data[i]['content']

    for tag in json_Lighttag_data[i]['annotations']:

        st = int(tag['start'])
        en = int(tag['end'])
        if(tag['value'] != tweet_text[st:en]):
            print(tweet_text)
            print(tweet_text[st:en], st, en)
            print(tag['value'])
            print(json_Lighttag_data[i]['tweetId'])

        # determine the type of tag label
        if(tag['tag'] == 'type of impact'):
            entity_tags['entities'].append((tag['start'], tag['end'],"IMPACT"))
        elif(tag['tag'] == 'item affected'):
            entity_tags['entities'].append((tag['start'], tag['end'],"AFFECTED"))
        elif(tag['tag'] == 'severity or quantity'):
            entity_tags['entities'].append((tag['start'], tag['end'],"SEVERITY"))  
        elif(tag['tag'] == 'place name'):
            entity_tags['entities'].append((tag['start'], tag['end'],"LOCATION"))
        elif(tag['tag'] == 'location modifier'):
            entity_tags['entities'].append((tag['start'], tag['end'],"MODIFIER"))
        else:
            print(tag['tag'])
            print(tweet_text)
        light_tag_count += 1 
        
        
    # determine the tweets that are validation or training
    # these are the same groups as for MT
    if(tweet_count > (total_LightTag_tweets/10) * TEN_FOLD_ROUND_NUM) and (tweet_count < (total_LightTag_tweets/10) * (TEN_FOLD_ROUND_NUM + 1)):
        validation_data.append((tweet_text,entity_tags))
    else:
        training_data.append((tweet_text,entity_tags))
    entity_tags = {'entities':[]}
    tweet_count+=1

print("tweet count", tweet_count)
print("t, v",len(training_data), len(validation_data))
print("total",len(training_data) + len(validation_data))
print("light tag count",light_tag_count)

print("total tag count",light_tag_count+mt_tag_count)


# random.shuffle(training_data)
print ("--")
none_count = 0
none_type = {"IMPACT": 0, "AFFECTED" : 0, "SEVERITY" : 0, "LOCATION": 0, "MODIFIER": 0}
count = 0
nlp = spacy.blank("en")

db_train = DocBin()
db_dev = DocBin()

# training data creation .spacy file
for text, annotations in training_data:
    
    doc_train = nlp(text)
    ents_train = []

    for start, end, label in annotations['entities']:
        
        span = doc_train.char_span(int(start), int(end), label=label, alignment_mode="strict")
        # alignment_mode="strict" has no token snapping
        # alignment_mode="contract" has span of all tokens completely within the character span

        if str(span) == "None":
            # If words lack spaces around them the span returns None

            # insert spaces into text
            newtext = text[0:int(start)] + " " + text[int(start):int(end)] + " " + text[int(end):]
           
            none_type[label] += 1
            none_count += 1

            # Train on new text
            doc_train = nlp(newtext)
            newspan = doc_train.char_span(int(start)+1, int(end)+1, label=label, alignment_mode="strict")

            if(str(newspan) != "None"):
                # append here if including the items that used to be none
                # ents_train.append(newspan)

                # none_type[label] -= 1
                # none_count -= 1
                count+=1

        else:
            ents_train.append(span)
            count += 1
    
    # creation of the .spacy training file
    ents_train_filtered = filter_spans(ents_train)
    doc_train.ents = ents_train_filtered
    db_train.add(doc_train)

# testing/validation data creation .spacy file
for text, annotations in validation_data:
    
    doc_dev = nlp(text)
    ents_dev = []

    for start, end, label in annotations['entities']:
        
        span = doc_dev.char_span(int(start), int(end), label=label, alignment_mode="strict")
        # alignment_mode="strict" has no token snapping
        # alignment_mode="contract" has span of all tokens completely within the character span

        # print(span)
        if str(span) == "None":
            # If words lack spaces around them the span returns None

            # insert spaces into text
            newtext = text[0:int(start)] + " " + text[int(start):int(end)] + " " + text[int(end):]

            none_type[label] += 1
            none_count += 1

            # train on new text with spaces now inserted
            doc_dev = nlp(newtext)
            newspan = doc_dev.char_span(int(start)+1, int(end)+1, label=label, alignment_mode="strict")

            if(str(newspan) != "None"):
                # append here if including the items that used to be none
                # ents_dev.append(newspan)

                # none_type[label] -= 1
                # none_count -= 1
                count+=1

        else:
            count += 1
            ents_dev.append(span)

    # testing .spacy file 
    ents_dev_filtered = filter_spans(ents_dev)
    doc_dev.ents = ents_dev_filtered
    db_dev.add(doc_dev)


# db_dev.to_disk("./testing/dev_{}.spacy".format(TEN_FOLD_ROUND_NUM))
# db_train.to_disk("./training/train_{}.spacy".format(TEN_FOLD_ROUND_NUM))
db_dev.to_disk("./testing-none-ex/dev_{}.spacy".format(TEN_FOLD_ROUND_NUM))
db_train.to_disk("./training-none-ex/train_{}.spacy".format(TEN_FOLD_ROUND_NUM))
# db_dev.to_disk("./dev.spacy")
# db_train.to_disk("./train.spacy")
# output to different locations dependent on 10 fold validation or not

print("count", count)
print("none_count", none_count)
print(none_type)
