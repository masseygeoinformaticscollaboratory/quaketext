import json
from nltk.tokenize import SpaceTokenizer
# from nltk.tokenize.stanford import StanfordTokenizer
import random
import re

# tk = StanfordTokenizer()

individual_tags = {"type of impact":[], "item affected":[],"severity or quantity":[],"place name":[],"location modifier":[]}

impact_dict = {"type of impact": "IMPACT", "item affected" : "AFFECTED", "severity or quantity" : "SEVERITY", "place name": "LOCATION", "location modifier": "MODIFIER"}

training_MT_file = open('../CSVtoJSONcode/finaltags.json')
json_MT_data = json.load(training_MT_file)

training_Lighttag_file = open('../CSVtoJSONcode/lighttag_finaltags.json')
json_Lighttag_data = json.load(training_Lighttag_file)

# train_bio_file = open("train_bio_tagged_data_MT.tsv", 'w', encoding = 'utf-8')
# dev_bio_file = open("dev_bio_tagged_data_MT.tsv", 'w', encoding = 'utf-8')

test_data_file = open("bio_test.txt", 'w', encoding = 'utf-8')

def new_file_location(file_count,data_origin):
    file = open("./bio_data/{}_0{}.txt".format(data_origin, file_count), 'w', encoding = 'utf-8')
    # file = open("./individual_tags_bio_files/impact/{}_0{}.txt".format(data_origin, file_count), 'w', encoding = 'utf-8')

    return file

def build_bio_files(json_data, type):

    print("length",len(json_data))

    shuffle_json_keys = list(json_data.keys())
    # random.shuffle(shuffle_json_keys)

    file_count = 0
    tag_count = 0
    total_tweets = 0
    bio_tag = ""
    foundTag = False
    lastVal = ""
    tweet_count = 0
    bio_file = new_file_location(file_count,type)

    for i in shuffle_json_keys:
        # print(json_data[i]['content'])

        if(tweet_count > len(json_data)/10):
            file_count+=1
            bio_file = new_file_location(file_count, type)
            total_tweets += tweet_count
            tweet_count = 0
        if(total_tweets > ((len(json_data)/10) * 9)):
            test_data_file.write(json_data[i]['content'])


        tweet_text = json_data[i]['content']

        # txt = re.split('\s',tweet_text)
        # print (tweet_text)

        # text = tk.tokenize(tweet_text)
        

        # for word in re.split('\s|, |: |- |"|\'',tweet_text): #original files
        for word in re.split("\s|(#)|(, )|(:)|(;)|(- )|(\")|(\. )|(\.\Z)",tweet_text):
        # for word in txt:
            # print(word)
            for tag in json_data[i]['annotations']:
                # print(tag['tag'])

                j = 0
                for each_tag in re.split("\s|, ",tag['value']):
                    # print(tag['value'])
                    # print(each_tag)
                    # print(word)
                    if str(word) != "None" and each_tag == word:
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
            if word != "" and str(word) != "None":

                # if "IMPACT" not in bio_tag:
                #     bio_tag = "O"
                    
                bio_file.write(word + "\t" + bio_tag + "\n")

        tweet_count += 1
        bio_file.write("\n")

    print(type)
    print("tweet count",tweet_count)
    print("total tweets",total_tweets + tweet_count)
    print("tag count",tag_count)

    bio_file.close()


build_bio_files(json_MT_data, "MT")
build_bio_files(json_Lighttag_data, "LightTag")