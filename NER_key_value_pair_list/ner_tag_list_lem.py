import json
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
  
lemmatizer = WordNetLemmatizer()
stemmer = PorterStemmer()

print("collapsed :", lemmatizer.lemmatize("collapse"))
print("corpora :", lemmatizer.lemmatize("corpora", pos="a"))

impact_list = ['cancellation','closure','collapse','damage','dead','death','delay','die','disruption','destroy','down','injured','injury','injuries','lose','loss','loss of life','malfunction','miss work','missing','no access','obstruction','rescue','stranded','theft','trap', 'kill']

lemmatized_impact_list = []
stemmer_impact_list = []

for item in impact_list:
    if lemmatizer.lemmatize(item) not in lemmatized_impact_list:
        lemmatized_impact_list.append(lemmatizer.lemmatize(item))
    if stemmer.stem(item) not in stemmer_impact_list:
            stemmer_impact_list.append(stemmer.stem(item))

print(lemmatized_impact_list)
print(stemmer_impact_list)
  
# Opening JSON file
MT_finaltags_file = open('../CSVtoJSONcode/finaltags.json')

json_file_path = "../CSVtoJSONcode/mt_combined.json"

impact_list_dict = {}

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


for tweet in impact_list_dict:
    # print(impact_list_dict[tweet])
    impact_list_dict[tweet]['tag'] = []

    lowercase_tweet = impact_list_dict[tweet]['text'].lower() # can use this to tse TODO!
    # print(lowercase_tweet)
    lemmatized_tweet = []
    stemmer_tweet = []
    words = word_tokenize(lowercase_tweet)
    for word in words:
        # print(word, ": ", stemmer.stem(word))
        lemmatized_tweet.append(lemmatizer.lemmatize(word))
        stemmer_tweet.append(stemmer.stem(word))

    # print("lowercase_tweet",lowercase_tweet)
    # print("lem_tweet: ",lemmatized_tweet)
    # print("ste_tweet: ",stemmer_tweet)

    # for impact in stemmer_impact_list:       
    #     for word in stemmer_tweet:
    #         if impact == word:

    #             # print("tweet: ",stemmer_tweet)
    #             # print("found impact = " + impact)

    #             start = lowercase_tweet.find(impact)
    #             end = lowercase_tweet.rfind(impact)
            
    #             current_tags = impact_list_dict[tweet]['tag']
    #             current_tags.extend([{'value':impact,'start':str(start),"found": "null"}])
    #             impact_list_dict[tweet]['tag'] = current_tags

    for impact in lemmatized_impact_list:
        for word in lemmatized_tweet:
            if impact == word:

                # print("tweet: ",lemmatized_tweet)
                # print("found impact = " + impact)

                start = lowercase_tweet.find(impact)
                end = lowercase_tweet.rfind(impact)
            
                current_tags = impact_list_dict[tweet]['tag']
                current_tags.extend([{'value':impact,'start':str(start),"found": "null"}])
                impact_list_dict[tweet]['tag'] = current_tags
    


  
# returns JSON object as 
# a dictionary
MT_data = json.load(MT_finaltags_file)

LT_finaltags_file = open('../CSVtoJSONcode/lighttag_finaltags.json')

LT_data = json.load(LT_finaltags_file)

MT_data.update(LT_data)
  
# Iterating through the json MT file for gold standard final tags
# list

print("hello world")

true_pos = 0 # tagged correctly
false_neg = 0 
false_pos = 0

found = False

count = 0
for tweet in MT_data:
    # print(data[i]['annotations'])
    # impact_only_dict = {}
    for anno in MT_data[tweet]['annotations']:
        if anno['tag'] == "type of impact":

            for i in impact_list_dict[tweet]['tag']:
                # print("inside for ",i)
                if(i['start'] == anno['start']):
                    true_pos += 1
                    i['found'] = "yes"
                    found = True
            
            if(found == False):
                # word was not found
                # print("false negative",anno)
                false_neg+= 1
            
            found = False
            # print(i)
            # print(anno)
            count = count+1

for tweet in impact_list_dict:
    for tag in impact_list_dict[tweet]['tag']:
        if tag['found'] == "null":
            # print("false positive",tag)
            # print(impact_list_dict[tweet]['text'])
            false_pos+= 1

# TODO need to read in tagged data to compare only impact tags
# Read in tweets to see if value list is contained within
# if it is then get start and end and compare with tagged dataset?

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


# Closing file
MT_finaltags_file.close()