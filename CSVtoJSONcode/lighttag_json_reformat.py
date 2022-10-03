
from __future__ import annotations
import csv
import json

MIN_THRESHOLD = 3



def save_tweet_tag_count(instance_dict):

    # print(instance_dict)
    # print("from function")

    for i in instance_dict:
        if i != 'tweetId' and i != 'tweetText':
            # print(i)

            instance = instance_dict[i][0]
            label = instance_dict[i][1]
            count = str(instance_dict[i][2])
            start = str(instance_dict[i][3])
            end = str(instance_dict[i][4])

            if(start == end):
                print("here", label)
            

            csv_tag_count_file.write(instance_dict['tweetId'] + "\t" + label + "\t" + instance + "\t"+ count + "\t"+ start + "\t"+ end + "\t"+  instance_dict['tweetText'] + "\n")


# ----------------------------------------------------------------------------------
# output from convertCSVtoJSON - in this case mt_combined.json
light_tag_json_file_path = "lighttag-800-tweets-annotated.json" # input('Enter the absolute path of the INPUT JSON file: ')
csv_file_path = "light_tag_results.csv" # input('Enter the absolute path of the OUTPUT CSV file: ')

instance_dict = {}

csv_worker_tags_file = open(csv_file_path, 'w', encoding = 'utf-8')
csv_worker_tags_file.write('AssignmentStatus' + "\t" + 'tweet_id' + "\t" + 'num taggers' + "\t" + 'label' + "\t" + 'instance' +"\t" + 'startOffset' +"\t" + 'endOffset' +"\t" + 'Input.text' +"\t" + 'Answer.taskAnswers' + "\n")

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

                status = True

                if (tag['correct'] == False):
                    status = False

                csv_worker_tags_file.write(str(status) + "\t" + tweet['metadata']['tweet_id'] + "\t" + str(len(tag['annotated_by'])) + "\t" + tag['tag'] + "\t" + tag['value'] + "\t" + str(tag['start']) + "\t" + str(tag['end']) + "\t" + tweet['content'] + "\t" + "\n")


            count += 1

        # if count == 0:
        #     instance_dict.update({"tweetId" : i['Input.id']})
        #     instance_dict.update({"tweetText" : i['Input.text']})
        #     # print(instance_dict)
        # elif instance_dict["tweetId"] != i['Input.id']:
        #     # reached a new tweet id file row - change dictionary
            
        #     # writing to tag_count file once all the tags for that tweet have been read
        #     # save_tweet_tag_count(instance_dict)

        #     instance_dict.clear()
        #     instance_dict.update({"tweetId" : i['Input.id']})
        #     instance_dict.update({"tweetText" : i['Input.text']})
        #     # print(instance_dict)
        # # else:
        # #     # tweet ID is the same use existing counts

        # # if the MT tag is approved  
        # if i['AssignmentStatus'] == "Approved":
            
        #     task_object = json.loads(i['Answer.taskAnswers'])

        #     name = 'annotation-tweet-id-'+ i['Input.id']

        #     entitiesPresent = False

        #     # https://stackoverflow.com/questions/24708634/python-and-json-typeerror-list-indices-must-be-integers-not-str
        #     for tag in task_object[0][name]['entities']:
        #         # for all the entities if there are any
        #         entitiesPresent = True
                
        #         start = tag['startOffset']
        #         end = tag['endOffset']

        #         # https://www.pythoncentral.io/cutting-and-slicing-strings-in-python/
        #         instance = i['Input.text'][start:end]

        #         # removing edge whitespace from the tag
        #         letter_count = 0
        #         string_length = len(instance)

        #         for letter in instance:
        #             if letter == ' ':

        #                 if(letter_count == 0):
        #                     # print("inbefore-" + instance + "-")
        #                     instance = instance.lstrip()
        #                     # print("inafter-" + instance + "-")
        #                     start = start + 1
        #                     string_length = string_length = 1
                        
        #                 elif(letter_count == string_length - 1):
        #                     # print("before-" + instance + "-")
        #                     instance = instance.rstrip()
        #                     # print("after-" + instance + "-")
        #                     end = end - 1
                    
        #             letter_count += 1
                
        #         # -------------------------------------------------
                
        #         if start != end:
        #             # if in the case that an empty space was tagged
        #             csv_worker_tags_file.write(i['AssignmentStatus'] + "\t" + i['Input.id'] + "\t" + i['WorkerId'] + "\t" + tag['label'] + "\t" + instance + "\t" + str(start) + "\t" + str(end) + "\t" + i['Input.text'] + "\t" + i['Answer.taskAnswers'] + "\n")
        #             count = count + 1

        #             instance_count = 1
        #             key = instance+"-"+tag['label']+"-"+str(start)+"-"+str(end)

        #             curr_dict_state = instance_dict.keys()

        #             if key in curr_dict_state:
        #                 # if it exists in the instance_dict add one to the count
        #                 instance_count = instance_dict[key][2] + 1

        #             instance_dict.update({key:[instance, tag['label'], instance_count, start, end]})

        #     if entitiesPresent == False:
        #         csv_worker_tags_file.write(i['AssignmentStatus'] + "\t" + i['Input.id'] + "\t" + i['WorkerId'] + "\t" + "\t" + "\t" + "\t" + "\t" + i['Input.text'] + "\t" + i['Answer.taskAnswers'] + "\n")

        #     entitiesPresent = False
            

        # # only look at accepted tags from approved tasks
        # # extracting of the words - new line for each?
        # else:
        #     csv_worker_tags_file.write(i['AssignmentStatus'] + "\t" + i['Input.id'] + "\t" + i['WorkerId'] + "\n")


    # last save for last tweet in file
    save_tweet_tag_count(instance_dict)
    print(count)

csv_worker_tags_file.close()
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
        print(rows)

        if(rows['AssignmentStatus'] != "False"):
                
            if first == True:
             # if the first row in the file, that is the current
                currentId = rows['tweet_id']
                currentText = rows['Input.text']
                light_dict[currentId] = ({"tweetId":currentId, "content": currentText,})
                light_dict[currentId]["annotations"] = []
                first = False 
                total_tweet_count += 1      
            elif currentId != rows['tweet_id']:
            # if the ids do not match then all the annotations for the previous tweet have been read save to dictionary and change current it and text, and clear annotation list for new tweet 
                currentId = rows['tweet_id']
                currentText = rows['Input.text']
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

            light_dict[currentId]["annotations"] = (current_annotation_state + [{"tag": rows['label'],"count": rows['num taggers'],"value": rows['instance'], "start": rows['startOffset'],"end": rows['endOffset']}])


    print("total tweet count = " + str(total_tweet_count))

            

# # add dictionary to json file
json_lightTag_format = "lighttag_finaltags.json"
with open(json_lightTag_format, 'w', encoding = 'utf-8') as json_file:
    json_file.write(json.dumps(light_dict, indent = 4))


