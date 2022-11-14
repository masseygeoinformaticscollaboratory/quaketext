# reviewing tags for approval in mechanical turk
import json

json_file_path = input('Path of the MT output JSON file: ')
# review3.json made from convertCSVtoJSON.py
csv_file_path = "batch_3_all_tags_with_workers.csv" 

instance_dict = {}

csv_worker_tags_file = open(csv_file_path, 'w', encoding = 'utf-8')
csv_worker_tags_file.write('AssignmentStatus' + "\t" + 'Input.id' + "\t" + 'WorkerId' + "\t" + 'label' + "\t" + 'instance' +"\t" + 'startOffset' +"\t" + 'endOffset' +"\t" + 'Input.text' +"\t" + 'Answer.taskAnswers' + "\n")


with open(json_file_path, encoding = 'utf-8') as json_file_handler:
    
    data = json.load(json_file_handler)

    count = 0

    for i in data.values():

        if count == 0:
            instance_dict.update({"tweetId" : i['Input.id']})
            instance_dict.update({"tweetText" : i['Input.text']})
            
        elif instance_dict["tweetId"] != i['Input.id']:
            instance_dict.clear()
            instance_dict.update({"tweetId" : i['Input.id']})
            instance_dict.update({"tweetText" : i['Input.text']})

     
        if i['AssignmentStatus'] == "Submitted":
            count = count + 1
       
            task_object = json.loads(i['Answer.taskAnswers'])

            name = 'annotation-tweet-id-'+ i['Input.id']

            entitiesPresent = False

            for tag in task_object[0][name]['entities']:
                entitiesPresent = True
                

                start = tag['startOffset']
                end = tag['endOffset']

                instance = i['Input.text'][start:end]                

                csv_worker_tags_file.write(i['AssignmentStatus'] + "\t" + i['Input.id'] + "\t" + i['WorkerId'] + "\t" + tag['label'] + "\t" + instance + "\t" + str(tag['startOffset']) + "\t" + str(tag['endOffset']) + "\t" + i['Input.text'] + "\t" + i['Answer.taskAnswers'] + "\n")

                num = 1
                key = instance+"-"+tag['label']+"-"+str(start)+"-"+str(end)

                curr_dict_state = instance_dict.keys()

                if key in curr_dict_state:
                    num = instance_dict[key][2] + 1

                instance_dict.update({key:[instance, tag['label'], num, start, end]})


            if entitiesPresent == False:
                csv_worker_tags_file.write(i['AssignmentStatus'] + "\t" + i['Input.id'] + "\t" + i['WorkerId'] + "\t" + "\t" + "\t" + "\t" + "\t" + i['Input.text'] + "\t" + i['Answer.taskAnswers'] + "\n")

            entitiesPresent = False
            

        # only look at accepted tags from approved tasks
        # extracting of the words - new line for each?
        else:
            csv_worker_tags_file.write(i['AssignmentStatus'] + "\t" + i['Input.id'] + "\t" + i['WorkerId'] + "\n")


    # last save for last tweet in file
    # print(count)

csv_worker_tags_file.close()



