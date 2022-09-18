# https://www.askpython.com/python/examples/convert-csv-to-json

import csv
from html import entities
import json
import re

def save_tweet_tag_count(instance_dict):

    print(instance_dict)
    print("from function")

    for i in instance_dict:
        if i != 'tweetId' and i != 'tweetText':
            print(i)

            instance = instance_dict[i][0]
            label = instance_dict[i][1]
            count = str(instance_dict[i][2])
            start = str(instance_dict[i][3])
            end = str(instance_dict[i][4])

            csv_tag_count_file.write(instance_dict['tweetId'] + "\t" + label + "\t" + instance + "\t"+ count + "\t"+ start + "\t"+ end + "\t"+  instance_dict['tweetText'] + "\n")


json_file_path = input('Enter the absolute path of the INPUT JSON file: ')
csv_file_path = input('Enter the absolute path of the OUTPUT CSV file: ')

instance_dict = {}

csv_worker_tags_file = open(csv_file_path, 'w', encoding = 'utf-8')
csv_worker_tags_file.write('AssignmentStatus' + "\t" + 'Input.id' + "\t" + 'WorkerId' + "\t" + 'label' + "\t" + 'instance' +"\t" + 'startOffset' +"\t" + 'endOffset' +"\t" + 'Input.text' +"\t" + 'Answer.taskAnswers' + "\n")

csv_tag_count_file = open("tagcount.csv", 'w', encoding = 'utf-8')
csv_tag_count_file.write('tweetId' + "\t" + 'label' + "\t" + 'instance' + "\t"+ 'count' + "\t"+ 'start' + "\t"+ 'end' + "\t"+'tweetText' + "\n")
 
with open(json_file_path, encoding = 'utf-8') as json_file_handler:
    
    data = json.load(json_file_handler)

    count = 0

    # https://stackoverflow.com/questions/41445573/python-loop-through-json-file
    for i in data.values():

        if count == 0:
            instance_dict.update({"tweetId" : i['Input.id']})
            instance_dict.update({"tweetText" : i['Input.text']})
            # print(instance_dict)
        elif instance_dict["tweetId"] != i['Input.id']:
            # new tweet change dictionary
            
            save_tweet_tag_count(instance_dict)

            instance_dict.clear()
            instance_dict.update({"tweetId" : i['Input.id']})
            instance_dict.update({"tweetText" : i['Input.text']})
            # print(instance_dict)
        else:
            # tweet ID is the same use existing counts
            print("same")

     
        if i['AssignmentStatus'] == "Approved":
            count = count + 1
            # print(i['WorkerId'])

            # print(i['Answer.taskAnswers'])

            # print()

       
            task_object = json.loads(i['Answer.taskAnswers'])

            name = 'annotation-tweet-id-'+ i['Input.id']

            print(name)
            print()

            entitiesPresent = False

            # https://stackoverflow.com/questions/24708634/python-and-json-typeerror-list-indices-must-be-integers-not-str
            for tag in task_object[0][name]['entities']:
                entitiesPresent = True
                # print(tag['endOffset'])
                # print("===")
                # print(tag['label'])
                # print("==")
                # print(tag['startOffset'])
                # print("=")
                # print()

                start = tag['startOffset']
                end = tag['endOffset']

                # https://www.pythoncentral.io/cutting-and-slicing-strings-in-python/
                instance = i['Input.text'][start:end]

                print(instance)

                csv_worker_tags_file.write(i['AssignmentStatus'] + "\t" + i['Input.id'] + "\t" + i['WorkerId'] + "\t" + tag['label'] + "\t" + instance + "\t" + str(tag['startOffset']) + "\t" + str(tag['endOffset']) + "\t" + i['Input.text'] + "\t" + i['Answer.taskAnswers'] + "\n")

                num = 1
                key = instance+"-"+tag['label']+"-"+str(start)+"-"+str(end)

                curr_dict_state = instance_dict.keys()

                if key in curr_dict_state:
                    num = instance_dict[key][2] + 1

                instance_dict.update({key:[instance, tag['label'], num, start, end]})
                print("dictonary")
                print(instance_dict)


            if entitiesPresent == False:
                csv_worker_tags_file.write(i['AssignmentStatus'] + "\t" + i['Input.id'] + "\t" + i['WorkerId'] + "\t" + "\t" + "\t" + "\t" + "\t" + i['Input.text'] + "\t" + i['Answer.taskAnswers'] + "\n")

            entitiesPresent = False
            

        # only look at accepted tags from approved tasks
        # extracting of the words - new line for each?
        else:
            csv_worker_tags_file.write(i['AssignmentStatus'] + "\t" + i['Input.id'] + "\t" + i['WorkerId'] + "\n")


    # last save for last tweet in file
    save_tweet_tag_count(instance_dict)
    print(count)

csv_worker_tags_file.close()
csv_tag_count_file.close()



# ---------------------------------------------------------------
# Checking agreement from the 5 taggers

with open("tagcount.csv", 'r', encoding = 'utf-8') as csv_file:
    
    agreement_dict = {}

    csv_reader = csv.DictReader(csv_file, delimiter='\t')

    first = True
    currentId = ""
    currentText = ""
    tagCount = 0

    for rows in csv_reader:
                
        if first == True:
            # if the first row in the file, that is the current
            currentId = rows['tweetId']
            currentText = rows['tweetText']
            agreement_dict[currentId] = ({"tweetId":currentId, "tweetText": currentText,})
            agreement_dict[currentId]["annotations"] = []
            first = False       
        elif currentId != rows['tweetId']:
            # if the ids do not match then all the annotations for the previous tweet have been read save to dictionary and change current it and text, and clear annotation list for new tweet 
            currentId = rows['tweetId']
            currentText = rows['tweetText']
            agreement_dict[currentId] = ({"tweetId":currentId, "tweetText": currentText,})
            agreement_dict[currentId]["annotations"] = []

            tagCount = 0
            print("new id")


        instance_count = int(rows['count'])
        print(tagCount)

        if instance_count >= 3:

            current_annotation_state = agreement_dict[currentId]["annotations"]
            print("curr state")
            print(current_annotation_state)

            agreement_dict[currentId]["annotations"] = (current_annotation_state + [{"label": rows['label'],"count": rows['count'],"instance": rows['instance'], "start": rows['start'],"end": rows['end']}])


        tagCount += 1

            

# add dictionary to json file
with open("finaltags.json", 'w', encoding = 'utf-8') as json_file:
    json_file.write(json.dumps(agreement_dict, indent = 4))


