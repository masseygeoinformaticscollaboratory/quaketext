# Takes in the unfiltered JSON input from MT to convert into the finaltags.json files that are used for later NER processing
import csv
import json

include_empty_tweets = False

# the minimum number of tag counts to accept for the final tag file
MIN_THRESHOLD = 3

# if there are overlapping tags increase count for overlapping sections
def check_for_overlapping_tags(instance_dict, count):

    # create empty dictionary to store each instance under each label
    label_type_dict = {"type of impact" : [],"item affected" : [],"severity or quantity" : [],"place name" : [],"location modifier" : [],}

    # for each tag that is in the current tweet, loop through and store any that are under the minimum threshold to the label dictionary
    for i in instance_dict:
        if i != 'tweetId' and i != 'tweetText':

            instance = instance_dict[i][0]
            label = instance_dict[i][1]
            count = str(instance_dict[i][2])
            start = str(instance_dict[i][3])
            end = str(instance_dict[i][4])

            if(int(count) < MIN_THRESHOLD):
                label_type_dict[label].append({'instance':instance,'count':count,'label':label,'start':start,'end':end})

    # loops through each label category type: impact, place name etc
    for category in label_type_dict:
        # print(category)
        top_item = ""
        top_count = 0
        top = {}
        
        # loops through each tag in current category
        for x in label_type_dict[category]:
            # print(x)
            curr_count = 0
            current_item = x['instance']
            # print(current_item)
            
            # for the current tag item compare to the others in the current label category 
            for y in label_type_dict[category]:
                
                if(y['instance'] == current_item): 
                    # if they are the same add current count
                    curr_count = curr_count + int(y['count'])
                else:
                    # else check if current tag is within the comparison tag
                    if current_item in y['instance']:
                        # if it is, then add to count
                        # print(y['instance'])
                        curr_count = curr_count + int(y['count'])
            
            if(curr_count > top_count):
                top_count = curr_count
                top_item = current_item
                top = x
        
        if(top_count > 0):
            # update the instance dictionary with a new count if other tags have that text inside them

            key = top_item+"-"+top['label']+"-"+str(top['start'])+"-"+str(top['end'])

            instance_dict.update({key:[top_item, top['label'], top_count, str(top['start']), str(top['end'])]})


# saving tag count value into csv file
def save_tweet_tag_count(instance_dict):
    found = False

    for i in instance_dict:
        
        if i != 'tweetId' and i != 'tweetText':
            found = True

            instance = instance_dict[i][0]
            label = instance_dict[i][1]
            count = str(instance_dict[i][2])
            start = str(instance_dict[i][3])
            end = str(instance_dict[i][4])

            if(start == end):
                print("here", label)
            
            csv_tag_count_file.write(instance_dict['tweetId'] + "\t" + label + "\t" + instance + "\t"+ count + "\t"+ start + "\t"+ end + "\t"+  instance_dict['tweetText'] + "\n")
    
    if found == False and include_empty_tweets == True:
        csv_tag_count_file.write(instance_dict['tweetId'] + "\t" + "\t" + "\t"+ "0" + "\t"+ "\t"+ "\t"+  instance_dict['tweetText'] + "\n")


# ----------------------------------------------------------------------------------
# output from convertCSVtoJSON - in this case mt_combined.json
json_file_path = "mt_combined.json" 

csv_worker_file_path = "all_tags_with_workers.csv" 

instance_dict = {}

csv_worker_tags_file = open(csv_worker_file_path, 'w', encoding = 'utf-8')
csv_worker_tags_file.write('AssignmentStatus' + "\t" + 'Input.id' + "\t" + 'WorkerId' + "\t" + 'label' + "\t" + 'instance' +"\t" + 'startOffset' +"\t" + 'endOffset' +"\t" + 'Input.text' +"\t" + 'Answer.taskAnswers' + "\n")

csv_tag_path = "tagcount.csv"
if include_empty_tweets == True:
    csv_tag_path = "tagcount_all_tweets.csv"

csv_tag_count_file = open(csv_tag_path, 'w', encoding = 'utf-8')
csv_tag_count_file.write('tweetId' + "\t" + 'label' + "\t" + 'instance' + "\t"+ 'count' + "\t"+ 'start' + "\t"+ 'end' + "\t"+'tweetText' + "\n")
 
#  read in input json and output data to all_tags_with_workers.csv and tag_count.csv
with open(json_file_path, encoding = 'utf-8') as json_file_handler:
    
    data = json.load(json_file_handler)

    count = 0

    # https://stackoverflow.com/questions/41445573/python-loop-through-json-file
    for i in data.values():

        if count == 0:
            instance_dict.update({"tweetId" : i['Input.id']})
            instance_dict.update({"tweetText" : i['Input.text']})

        elif instance_dict["tweetId"] != i['Input.id']:
            # reached a new tweet id file row - change dictionary

            # Are there any tags that overlap and can increase their counts?
            check_for_overlapping_tags(instance_dict, count)
            
            # writing to tag_count file once all the tags for that tweet have been read
            save_tweet_tag_count(instance_dict)

            instance_dict.clear()
            instance_dict.update({"tweetId" : i['Input.id']})
            instance_dict.update({"tweetText" : i['Input.text']})

        # if the MT tag is approved  
        if i['AssignmentStatus'] == "Approved":
            
            task_object = json.loads(i['Answer.taskAnswers'])

            name = 'annotation-tweet-id-'+ i['Input.id']

            entitiesPresent = False

            # https://stackoverflow.com/questions/24708634/python-and-json-typeerror-list-indices-must-be-integers-not-str
            for tag in task_object[0][name]['entities']:
                # for all the entities if there are any
                entitiesPresent = True
                
                start = tag['startOffset']
                end = tag['endOffset']

                # https://www.pythoncentral.io/cutting-and-slicing-strings-in-python/
                instance = i['Input.text'][start:end]

                # removing edge whitespace from the tag at start or end if it was included in the tag itself
                letter_count = 0
                string_length = len(instance)

                for letter in instance:
                    if letter == ' ':

                        if(letter_count == 0):
                            instance = instance.lstrip()
                            start = start + 1
                            string_length = string_length = 1
                        
                        elif(letter_count == string_length - 1):
                            instance = instance.rstrip()
                            end = end - 1
                    
                    letter_count += 1
                
                # -------------------------------------------------
                
                if start != end:
                    # if in the case that an empty space was tagged
                    csv_worker_tags_file.write(i['AssignmentStatus'] + "\t" + i['Input.id'] + "\t" + i['WorkerId'] + "\t" + tag['label'] + "\t" + instance + "\t" + str(start) + "\t" + str(end) + "\t" + i['Input.text'] + "\t" + i['Answer.taskAnswers'] + "\n")
                    count = count + 1

                    instance_count = 1
                    key = instance+"-"+tag['label']+"-"+str(start)+"-"+str(end)

                    curr_dict_state = instance_dict.keys()

                    if key in curr_dict_state:
                        # if it exists in the instance_dict add one to the count
                        instance_count = instance_dict[key][2] + 1

                    instance_dict.update({key:[instance, tag['label'], instance_count, start, end]})

            if entitiesPresent == False:
                # no tags were found for this tweet
                csv_worker_tags_file.write(i['AssignmentStatus'] + "\t" + i['Input.id'] + "\t" + i['WorkerId'] + "\t" + "\t" + "\t" + "\t" + "\t" + i['Input.text'] + "\t" + i['Answer.taskAnswers'] + "\n")

            entitiesPresent = False
            

        # only look at accepted tags from approved tasks
        else:
            csv_worker_tags_file.write(i['AssignmentStatus'] + "\t" + i['Input.id'] + "\t" + i['WorkerId'] + "\n")


    # last save for last tweet in file with no change check of id
    save_tweet_tag_count(instance_dict)
    print(count)

csv_worker_tags_file.close()
csv_tag_count_file.close()



# ---------------------------------------------------------------
# Checking agreement from the 5 taggers from the tagcount.csv file

with open(csv_tag_path, 'r', encoding = 'utf-8') as csv_file:
    
    agreement_dict = {}
    final_dict = {}

    csv_reader = csv.DictReader(csv_file, delimiter='\t')

    first = True
    currentId = ""
    currentText = ""
    tagCount = 0
    total_tweet_count = 0

    for rows in csv_reader:
                
        if first == True:
            # if the first row in the file, that is the current
            currentId = rows['tweetId']
            currentText = rows['tweetText']
            agreement_dict[currentId] = ({"tweetId":currentId, "content": currentText,})
            agreement_dict[currentId]["annotations"] = []
            first = False 
            total_tweet_count += 1      
        elif currentId != rows['tweetId']:
            # if the ids do not match then all the annotations for the previous tweet have been read save to dictionary and change current it and text, and clear annotation list for new tweet 
            currentId = rows['tweetId']
            currentText = rows['tweetText']
            agreement_dict[currentId] = ({"tweetId":currentId, "content": currentText,})
            agreement_dict[currentId]["annotations"] = []

            tagCount = 0
            total_tweet_count += 1


        instance_count = int(rows['count'])

        if instance_count >= MIN_THRESHOLD:

            current_annotation_state = agreement_dict[currentId]["annotations"]

            agreement_dict[currentId]["annotations"] = (current_annotation_state + [{"tag": rows['label'],"count": rows['count'],"value": rows['instance'], "start": rows['start'],"end": rows['end']}])


        tagCount += 1
    
    final_dict = agreement_dict
    print("total tweet count = " + str(total_tweet_count))
    print(len(final_dict))

            

# add dictionary to json file
json_output = "finaltags.json"

if include_empty_tweets == True:
    json_output = "finaltags_all_tweets.json"

with open(json_output, 'w', encoding = 'utf-8') as json_file:
    json_file.write(json.dumps(final_dict, indent = 4))


