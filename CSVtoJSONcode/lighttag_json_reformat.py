
from __future__ import annotations
import csv
import json

include_empty_tweets = False

# -------------------------------------------------------------------------
light_tag_json_file_path = "lighttag-800-tweets-annotated.json" 
csv_file_path = "light_tag_results.csv" 

if(include_empty_tweets == True):
    csv_file_path = "light_tag_results_all_tweets.csv" 

light_tag_csv_file = open(csv_file_path, 'w', encoding = 'utf-8')
light_tag_csv_file.write('AssignmentStatus' + "\t" + 'tweetId' + "\t" + 'num taggers' + "\t" + 'label' + "\t" + 'instance' +"\t" + 'start' +"\t" + 'end' +"\t" + 'tweetText' + "\n")
 
#  read in input json and output data to light_tag_results.csv
with open(light_tag_json_file_path, encoding = 'utf-8') as json_file_handler:
    
    data = json.load(json_file_handler)

    count = 0
    tc = 0

    # https://stackoverflow.com/questions/41445573/python-loop-through-json-file
    for i in data['data']:
        print(i['id'])

        for tweet in i['examples']:
            # print (tweet['annotations'])
            is_tags = False

            for tag in tweet['annotations']:
                # print(tag)
                is_tags = True

                splice = tweet['content'][tag['start']:tag['end']]
                if(tag['value']!= splice):
                    print("tag value", tag['value'])
                    print("splice" , splice)

                status = True

                if (tag['correct'] == False):
                    status = False
                    tc -= 1

                light_tag_csv_file.write(str(status) + "\t" + tweet['metadata']['tweet_id'] + "\t" + str(len(tag['annotated_by'])) + "\t" + tag['tag'] + "\t" + tag['value'] + "\t" + str(tag['start']) + "\t" + str(tag['end']) + "\t" + tweet['content'] + "\n")
                tc += 1


            count += 1

            if(is_tags == False and include_empty_tweets == True):
                light_tag_csv_file.write("True" + "\t" + tweet['metadata']['tweet_id'] + "\t" + "\t" + "\t" + "\t"  + "\t" + "\t" + tweet['content'] + "\n")

    print(count)

light_tag_csv_file.close()
print("count tags",tc)

# # ---------------------------------------------------------------
light_dict = {}

with open(csv_file_path, 'r', encoding = 'utf-8') as csv_file:

    csv_reader = csv.DictReader(csv_file, delimiter='\t')

    first = True
    currentId = ""
    currentText = ""
    tagCount = 0
    total_tweet_count = 0

    for rows in csv_reader:
        # print(rows)
        foundid = False
                
        if first == True:
            # if the first row in the file, that is the current
            currentId = rows['tweetId']
            currentText = rows['tweetText']
            light_dict[currentId] = ({"tweetId":currentId, "content": currentText,})
            light_dict[currentId]["annotations"] = []
            first = False 
            total_tweet_count += 1      
        elif currentId != rows['tweetId']:
            # if the ids do not match then all the annotations for the previous tweet have been read save to dictionary and change current it and text, and clear annotation list for new tweet 
            currentId = rows['tweetId']
            currentText = rows['tweetText']

            for tweet in light_dict:
                if tweet == currentId:
                    any_annotations = light_dict[currentId]["annotations"]
                    # print(tweet)
                    # print(any_annotations)
                    foundid = True
            
            if(foundid == False):
                light_dict[currentId] = ({"tweetId":currentId, "content": currentText,})      
                light_dict[currentId]["annotations"] = []
                total_tweet_count += 1
            
            foundid = False

           

        if(rows['AssignmentStatus'] == "True"):
            foundtag = False

            current_annotation_state = light_dict[currentId]["annotations"]
            for each in current_annotation_state:
                if(rows['instance'] == each['value']):
                    foundtag = True
                    # tag already exists

            if(foundtag == False) and rows['label'] != "":
                # only add tags if they are unique
                tagCount += 1
                light_dict[currentId]["annotations"] = (current_annotation_state + [{"tag": rows['label'],"count": rows['num taggers'],"value": rows['instance'], "start": rows['start'],"end": rows['end']}])
        
    print("LT_tagcount" ,tagCount)
    print("total LT_tweet count = ",total_tweet_count)

csv_file.close()

# # add dictionary to json file
json_lightTag_format = "lighttag_finaltags.json"
if(include_empty_tweets == True):
    json_lightTag_format = "lighttag_finaltags_all_tweets.json"
with open(json_lightTag_format, 'w', encoding = 'utf-8') as json_file:
    json_file.write(json.dumps(light_dict, indent = 4))








# Currently only taking tweets that contain tags
# # create a joined CSV file for both lighttag and MT data
def create_joined_csv_for_LT_MT():

    final_tags_combined_csv = open("final_tags_combined_LT_MT.csv", 'w', encoding = 'utf-8')
    final_tags_combined_csv.write('source' + "\t" + 'tweetId' + "\t" + 'label' + "\t" + 'instance' +"\t" + 'start' +"\t" + 'end' +"\t" + 'tweetText'  + "\n")
    num = 0
    
    # lighttag data-------------------------------------------------------------------
    with open("lighttag_finaltags.json", encoding = 'utf-8') as json_file_h:
    
        LT_data = json.load(json_file_h)

        for LT_rows in LT_data.values():
        
            source = "lightTag"
            id = LT_rows['tweetId']
            tweet = LT_rows['content']

            for anno in LT_rows['annotations']:
                tag = anno['tag']
                value = anno['value']
                start = str(anno['start'])
                end = str(anno['end'])

                final_tags_combined_csv.write(source + "\t" + id + "\t" + tag + "\t"+    value + "\t" + start + "\t" + end + "\t" + tweet + "\n")


    # Mechanical Turk data----------------------------------------------------------
    with open("tagcount.csv", 'r', encoding = 'utf-8') as MT_csv_file:

        MT_csv_reader = csv.DictReader(MT_csv_file, delimiter='\t')

        for MT_rows in MT_csv_reader:

            if(int(MT_rows['count']) > 3):
           
                source = "MechanicalTurk"
                id = MT_rows['tweetId']
                label = MT_rows['label']
                instance = MT_rows['instance']
                start = str(MT_rows['start'])
                end = str(MT_rows['end'])
                tweet = MT_rows['tweetText']

                final_tags_combined_csv.write(source + "\t" + id + "\t" + label + "\t" +    instance + "\t" + start + "\t" + end + "\t" + tweet + "\n")
                num += 1
    
    print("MT num", num)

    

create_joined_csv_for_LT_MT()