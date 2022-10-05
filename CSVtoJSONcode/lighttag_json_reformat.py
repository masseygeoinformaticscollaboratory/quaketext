
from __future__ import annotations
import csv
import json

# ----------------------------------------------------------------------------------
# output from convertCSVtoJSON - in this case mt_combined.json
light_tag_json_file_path = "lighttag-800-tweets-annotated.json" # input('Enter the absolute path of the INPUT JSON file: ')
csv_file_path = "light_tag_results.csv" # input('Enter the absolute path of the OUTPUT CSV file: ')

instance_dict = {}

light_tag_csv_file = open(csv_file_path, 'w', encoding = 'utf-8')
light_tag_csv_file.write('AssignmentStatus' + "\t" + 'tweetId' + "\t" + 'num taggers' + "\t" + 'label' + "\t" + 'instance' +"\t" + 'start' +"\t" + 'end' +"\t" + 'tweetText' + "\n")

# csv_tag_count_file = open("tagcount.csv", 'w', encoding = 'utf-8')
# csv_tag_count_file.write('tweetId' + "\t" + 'label' + "\t" + 'instance' + "\t"+ 'count' + "\t"+ 'start' + "\t"+ 'end' + "\t"+'tweetText' + "\n")
 
#  read in input json and output data to all_tags_with_workers.csv and tag_count.csv
with open(light_tag_json_file_path, encoding = 'utf-8') as json_file_handler:
    
    data = json.load(json_file_handler)

    count = 0

    # https://stackoverflow.com/questions/41445573/python-loop-through-json-file
    for i in data['data']:
        print(i['id'])

        for tweet in i['examples']:
            # print (tweet['annotations'])

            for tag in tweet['annotations']:
                # print(tag)

                splice = tweet['content'][tag['start']:tag['end']]
                if(tag['value']!= splice):
                    print("tag value", tag['value'])
                    print("splice" , splice)

                status = True

                if (tag['correct'] == False):
                    status = False

                light_tag_csv_file.write(str(status) + "\t" + tweet['metadata']['tweet_id'] + "\t" + str(len(tag['annotated_by'])) + "\t" + tag['tag'] + "\t" + tag['value'] + "\t" + str(tag['start']) + "\t" + str(tag['end']) + "\t" + tweet['content'] + "\n")


            count += 1

    print(count)

light_tag_csv_file.close()
# csv_tag_count_file.close()



# # ---------------------------------------------------------------
# # Checking agreement from the 5 taggers

with open("light_tag_results.csv", 'r', encoding = 'utf-8') as csv_file:
    
    light_dict = {}

    csv_reader = csv.DictReader(csv_file, delimiter='\t')

    first = True
    currentId = ""
    currentText = ""
    tagCount = 0
    total_tweet_count = 0

    for rows in csv_reader:
        # print(rows)

        if(rows['AssignmentStatus'] != "False"):
                
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
                light_dict[currentId] = ({"tweetId":currentId, "content": currentText,})
                light_dict[currentId]["annotations"] = []

                tagCount = 0
                total_tweet_count += 1
            # print("new id")


            # instance_count = int(rows['count'])
            # print(tagCount)

            # if instance_count >= MIN_THRESHOLD:

            current_annotation_state = light_dict[currentId]["annotations"]
            # print("curr state")
            # print(current_annotation_state)

            light_dict[currentId]["annotations"] = (current_annotation_state + [{"tag": rows['label'],"count": rows['num taggers'],"value": rows['instance'], "start": rows['start'],"end": rows['end']}])


    print("total tweet count = " + str(total_tweet_count))

csv_file.close()

# # add dictionary to json file
json_lightTag_format = "lighttag_finaltags.json"
with open(json_lightTag_format, 'w', encoding = 'utf-8') as json_file:
    json_file.write(json.dumps(light_dict, indent = 4))




# # create a joined CSV file for both lighttag and MT data
def create_joined_csv_for_LT_MT():

    final_tags_combined_csv = open("final_tags_combined_LT_MT.csv", 'w', encoding = 'utf-8')
    final_tags_combined_csv.write('source' + "\t" + 'tweetId' + "\t" + 'label' + "\t" + 'instance' +"\t" + 'start' +"\t" + 'end' +"\t" + 'tweetText'  + "\n")
    num = 0
    
    # lighttag data-------------------------------------------------------------------
    with open("light_tag_results.csv", 'r', encoding = 'utf-8') as LT_csv_file:

        LT_csv_reader = csv.DictReader(LT_csv_file, delimiter='\t')

        for LT_rows in LT_csv_reader:
        

            if(LT_rows['AssignmentStatus'] == "True"):
           
                # if(num == 173):
                #     print (LT_rows)
                # if(num == 174):
                #     print (LT_rows)

                source = "lightTag"
                id = LT_rows['tweetId']
                label = LT_rows['label']
                instance = LT_rows['instance']
                start = str(LT_rows['start'])
                end = str(LT_rows['end'])
                tweet = LT_rows['tweetText']

                final_tags_combined_csv.write(source + "\t" + id + "\t" + label + "\t" +    instance + "\t" + start + "\t" + end + "\t" + tweet + "\n")

                # print(source)
                num += 1
                # print(num)

    # Mechanical Turk data----------------------------------------------------------
    with open("tagcount.csv", 'r', encoding = 'utf-8') as MT_csv_file:

        MT_csv_reader = csv.DictReader(MT_csv_file, delimiter='\t')

        for MT_rows in MT_csv_reader:
        

            if(int(MT_rows['count']) > 3):
           
                if(num < 17):
                    print (MT_rows)

                source = "MechanicalTurk"
                id = MT_rows['tweetId']
                label = MT_rows['label']
                instance = MT_rows['instance']
                start = str(MT_rows['start'])
                end = str(MT_rows['end'])
                tweet = MT_rows['tweetText']

                final_tags_combined_csv.write(source + "\t" + id + "\t" + label + "\t" +    instance + "\t" + start + "\t" + end + "\t" + tweet + "\n")

    

create_joined_csv_for_LT_MT()