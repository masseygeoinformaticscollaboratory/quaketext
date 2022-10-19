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

training_Lighttag_file = open('../CSVtoJSONcode/lighttag_finaltags.json')
json_Lighttag_data = json.load(training_Lighttag_file)

# train_bio_file = open("train_bio_tagged_data_MT.tsv", 'w', encoding = 'utf-8')
# dev_bio_file = open("dev_bio_tagged_data_MT.tsv", 'w', encoding = 'utf-8')

test_data_file = open("bio_test.txt", 'w', encoding = 'utf-8')

def new_file_location(file_count,data_origin):
    file = open("./bio_data/{}_0{}.txt".format(data_origin, file_count), 'w', encoding = 'utf-8')

    return file
# bio_file.write("word" + "\t" + "tag" + "\n")

def build_bio_files(json_data, type):

    print("length",len(json_data))


    file_count = 0
    tag_count = 0
    total_tweets = 0
    bio_tag = ""
    foundTag = False
    lastVal = ""
    tweet_count = 0
    bio_file = new_file_location(file_count,type)

    for i in json_data:
        # print(json_data[i]['content'])

        if(tweet_count > len(json_data)/10):
            file_count+=1
            bio_file = new_file_location(file_count, type)
            total_tweets += tweet_count
            tweet_count = 0
        if(total_tweets > ((len(json_data)/10) * 9)):
            test_data_file.write(json_data[i]['content'])


        tweet_text = json_data[i]['content']

        for word in re.split('\s|, |: |- |"|\'',tweet_text):
            # print(word)
            for tag in json_data[i]['annotations']:
                # print(tag['tag'])

                j = 0
                for each_tag in re.split(" ",tag['value']):
                    # print(tag['value'])
                    # print(each_tag)
                    if word == each_tag:
                        if(j == 0):
                            pre = "B-"
                        else:
                            pre = "I-"

                        bio_tag = pre + impact_dict[tag['tag']]
                        foundTag = True
                        tag_count += 1
                    j+=1

                # if word in tag['value'] and word != "":
                # if word == tag['value']:
                #     if(lastVal == tag['value']):
                #         pre = "I-"
                #     else:
                #         pre = "B-"

                #     lastVal = tag['value']
                #     bio_tag = pre + impact_dict[tag['tag']]
                #     foundTag = True
                #     mt_tag_count += 1


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
        bio_file.write("\n")

    print(type)
    print("tweet count",tweet_count)
    print("total tweets",total_tweets + tweet_count)
    print("tag count",tag_count)

    bio_file.close()


build_bio_files(json_MT_data, "MT")
build_bio_files(json_Lighttag_data, "LightTag")