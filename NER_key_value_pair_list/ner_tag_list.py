import json
import re

# created from the impact table
impact_list = ['cancellation','closure','collapse','damage','dead','death','delay','die','disruption','destroy','down','injured','injury','injuries','lose','loss','loss of life','malfunction','miss work','missing','no access','obstruction','rescue','stranded','theft','trap', 'kill']
  
# Opening JSON file
MT_finaltags_file = open('../CSVtoJSONcode/finaltags.json')

impact_list_dict = {}

with open("../CSVtoJSONcode/finaltags.json", encoding = 'utf-8') as json_handler:
    
    data = json.load(json_handler)
    for i in data.values():
        impact_list_dict.update({i['tweetId']:{"id" : i['tweetId'],"text" : i['content']}})
    print(len(impact_list_dict))

with open("../CSVtoJSONcode/lighttag_finaltags.json", encoding = 'utf-8') as json_handler:
    
    data = json.load(json_handler)
    for i in data.values():
        impact_list_dict.update({i['tweetId']:{"id" : i['tweetId'],"text" : i['content']}})
    print(len(impact_list_dict))


for tweet in impact_list_dict:
    # print(impact_list_dict[tweet])
    impact_list_dict[tweet]['tag'] = []
    for impact in impact_list:
        lowercase_tweet = impact_list_dict[tweet]['text'].lower() 
        # convert tweet to lowercase to catch any impacts that use capitalization

        # if re.search(impact, impact_list_dict[tweet]['text'], re.IGNORECASE):
        if impact in lowercase_tweet:

            start = lowercase_tweet.find(impact)

            end = lowercase_tweet.rfind(impact)
            
            current_tags = impact_list_dict[tweet]['tag']
            current_tags.extend([{'value':impact,'start':str(start),"found": "null"}])
            impact_list_dict[tweet]['tag'] = current_tags


    


  
# take MT tweets - add to dictionary
MT_data = json.load(MT_finaltags_file)

LT_finaltags_file = open('../CSVtoJSONcode/lighttag_finaltags.json')

LT_data = json.load(LT_finaltags_file)

# add light tag data
MT_data.update(LT_data)
  
# Iterating through the json final tags file for gold standard final tags
# list

true_pos = 0 # tagged correctly
false_neg = 0 
false_pos = 0

found = False

count = 0

# calculation for result metrics
for tweet in MT_data:

    for anno in MT_data[tweet]['annotations']:
        if anno['tag'] == "type of impact":

            for i in impact_list_dict[tweet]['tag']:
                # print("inside for ",i)
                if(i['start'] == anno['start']):
                    true_pos += 1
                    i['found'] = "yes"
                    found = True
                    # tag found - case of true positive
            
            if(found == False):
                # word was not found
                print("false negative",anno)
                false_neg+= 1
                # word exists in manual annotation not new tags
            
            found = False
            count = count+1

for tweet in impact_list_dict:
    for tag in impact_list_dict[tweet]['tag']:
        if tag['found'] == "null":
            # print("false positive",tag)
            # print(impact_list_dict[tweet]['text'])
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

with open("test_result_lowercase.json", 'w', encoding = 'utf-8') as json_file_handler:
    json_file_handler.write(json.dumps(impact_list_dict, indent = 4))


MT_finaltags_file.close()