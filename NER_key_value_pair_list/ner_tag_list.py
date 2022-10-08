import json
import csv
import re

impact_list = ['cancellation','closure','collapse','damage','dead','death','delay','die','disruption','destroy','down','injured','injury','injuries','lose','loss','loss of life','malfunction','miss work','missing','no access','obstruction','rescue','stranded','theft','trap', 'kill']
# missing capitalization of some impact instances
  
# Opening JSON file
MT_finaltags_file = open('../CSVtoJSONcode/finaltags.json')

json_file_path = "../CSVtoJSONcode/mt_combined.json"

impact_list_dict = {}


with open(json_file_path, encoding = 'utf-8') as json_handler:
    
    data = json.load(json_handler)

    count = 0
 
    for i in data.values():
        print(i['Input.id'])

        impact_list_dict.update({i['Input.id']:{"id" : i['Input.id'],"text" : i['Input.text']}})

        # count+=1
    
    print(impact_list_dict, count)

for tweet in impact_list_dict:
    print(impact_list_dict[tweet])
    impact_list_dict[tweet]['tag'] = []
    for impact in impact_list:
        lowercase_tweet = impact_list_dict[tweet]['text']

        # if re.search(impact, impact_list_dict[tweet]['text'], re.IGNORECASE):
        if impact in lowercase_tweet:
            print("found impact = " + impact)
            # start = impact_list_dict[tweet]['text'].find(impact)
            start = lowercase_tweet.find(impact)
            # print(start)
            # end = impact_list_dict[tweet]['text'].rfind(impact)
            end = lowercase_tweet.rfind(impact)
            
            # print(end)
            current_tags = impact_list_dict[tweet]['tag']
            current_tags.extend([{'value':impact,'start':str(start),"found": "null"}])
            impact_list_dict[tweet]['tag'] = current_tags
            # test_data_dict[tweet]['tag'] = [{'value':impact,'start':str(start)}]

    


  
# returns JSON object as 
# a dictionary
MT_data = json.load(MT_finaltags_file)

  
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
                print("inside for ",i)
                if(i['start'] == anno['start']):
                    true_pos += 1
                    i['found'] = "yes"
                    found = True
            
            if(found == False):
                # word was not found
                false_neg+= 1
            
            found = False
            print(i)
            print(anno)
            count = count+1

for tweet in impact_list_dict:
    for tag in impact_list_dict[tweet]['tag']:
        if tag['found'] == "null":
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

with open("test_result.json", 'w', encoding = 'utf-8') as json_file_handler:
    json_file_handler.write(json.dumps(impact_list_dict, indent = 4))


# Closing file
MT_finaltags_file.close()