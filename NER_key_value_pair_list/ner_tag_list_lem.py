# impact list matching of impact tags to those that are within a list of impacts.

import json
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
  
# utilizing other functions to enable lemmatization and stemming
lemmatizer = WordNetLemmatizer()
stemmer = PorterStemmer()

print("collapsed :", lemmatizer.lemmatize("collapse"))
print("corpora :", lemmatizer.lemmatize("corpora", pos="a"))

impact_list = ['cancellation','closure','collapse','damage','dead','death','delay','die','disruption','destroy','down','injured','injury','injuries','lose','loss','loss of life','malfunction','miss work','missing','no access','obstruction','rescue','stranded','theft','trap', 'kill']

lemmatized_impact_list = []
stemmer_impact_list = []

# creating new lists of impacts that have been pre processed by stemmer or lemmatizer
for item in impact_list:
    if lemmatizer.lemmatize(item) not in lemmatized_impact_list:
        lemmatized_impact_list.append(lemmatizer.lemmatize(item))
    if stemmer.stem(item) not in stemmer_impact_list:
            stemmer_impact_list.append(stemmer.stem(item))

print(lemmatized_impact_list)
print(stemmer_impact_list)
  
MT_finaltags_file = open('../CSVtoJSONcode/finaltags.json')

impact_list_dict = {}

# read tags from the finaltags.json files
with open("../CSVtoJSONcode/finaltags.json", encoding = 'utf-8') as json_handler:
    
    data = json.load(json_handler)
    for i in data.values():
        impact_list_dict.update({i['tweetId']:{"id" : i['tweetId'],"text" : i['content']}})
    # print(len(impact_list_dict))

with open("../CSVtoJSONcode/lighttag_finaltags.json", encoding = 'utf-8') as json_handler:
    
    data = json.load(json_handler)
    for i in data.values():
        impact_list_dict.update({i['tweetId']:{"id" : i['tweetId'],"text" : i['content']}})
    # print(len(impact_list_dict))


# loop through tweets to look for impact words that exist in the lists
for tweet in impact_list_dict:

    impact_list_dict[tweet]['tag'] = []

    lowercase_tweet = impact_list_dict[tweet]['text'].lower() 

    lemmatized_tweet = []
    stemmer_tweet = []
    words = word_tokenize(lowercase_tweet)
    for word in words:

        lemmatized_tweet.append(lemmatizer.lemmatize(word))
        stemmer_tweet.append(stemmer.stem(word))

    # print("lowercase_tweet",lowercase_tweet)
    # print("lem_tweet: ",lemmatized_tweet)
    # print("ste_tweet: ",stemmer_tweet)

    for impact in stemmer_impact_list:       
        for word in stemmer_tweet:
            if impact == word:
                # change in to == to swap between substring and equality matching

                # print("tweet: ",stemmer_tweet)
                # print("found impact = " + impact)

                start = int(lowercase_tweet.find(impact))
                end = lowercase_tweet.rfind(impact)

                # dont add repeated words of the same start location
                found = False
                for tag in impact_list_dict[tweet]['tag']:
                    print(tag)
                    if start == int(tag['start']):
                        found = True
            
                if found == False:
                    current_tags = impact_list_dict[tweet]['tag']
                    current_tags.extend([{'value':impact,'start':str(start),"found": "null"}])
                    impact_list_dict[tweet]['tag'] = current_tags

    # for impact in lemmatized_impact_list:
    #     for word in lemmatized_tweet:
    #         if impact == word:
    #             # change in to == to swap between substring and equality matching

    #             # print("tweet: ",lemmatized_tweet)
    #             # print("found impact = " + impact)

    #             start = lowercase_tweet.find(impact)
    #             end = lowercase_tweet.rfind(impact)
            
    #             # dont add repeated words of the same start location
    #             found = False
    #             for tag in impact_list_dict[tweet]['tag']:
    #                 print(tag)
    #                 if start == int(tag['start']):
    #                     found = True
            
    #             if found == False:
    #                 current_tags = impact_list_dict[tweet]['tag']
    #                 current_tags.extend([{'value':impact,'start':str(start),"found": "null"}])
    #                 impact_list_dict[tweet]['tag'] = current_tags
    


  
MT_data = json.load(MT_finaltags_file)

LT_finaltags_file = open('../CSVtoJSONcode/lighttag_finaltags.json')

LT_data = json.load(LT_finaltags_file)

MT_data.update(LT_data)
  
# calculations for result metrics
true_pos = 0 # tagged correctly
false_neg = 0 
false_pos = 0

found = False

count = 0
for tweet in MT_data:

    for anno in MT_data[tweet]['annotations']:
        if anno['tag'] == "type of impact":

            for i in impact_list_dict[tweet]['tag']:
                if(i['start'] == anno['start']):
                    true_pos += 1
                    i['found'] = "yes"
                    found = True
                    # tag found - case of true positive
            
            if(found == False):
                # print("false negative",anno)
                false_neg+= 1
                # word exists in manual annotation but not new tags
            
            found = False
            count = count+1

for tweet in impact_list_dict:
    for tag in impact_list_dict[tweet]['tag']:
        if tag['found'] == "null":
            # print("false positive",tag)
            false_pos+= 1
            # word was tagged but does not exist in manual annotation

# Comparing new impact data to only impact tags in the manual annotation set

print("true pos", true_pos)
print("false pos", false_pos)
print("false neg", false_neg)

precision = true_pos /(true_pos + false_pos)

recall = true_pos /( true_pos + false_neg)

f1score = 2 * ((precision*recall)/(precision+recall))

print ("precision", precision)

print ("recall", recall)

print("f1score", f1score)

with open("test_result_lemma.json", 'w', encoding = 'utf-8') as json_file_handler:
    json_file_handler.write(json.dumps(impact_list_dict, indent = 4))

MT_finaltags_file.close()