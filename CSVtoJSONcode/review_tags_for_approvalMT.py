import json

json_file_path = input('Path of the MT output JSON file: ')
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

                # removing edge whitespace from the tag
                # if(count < 50):
                letter_count = 0
                string_length = len(instance)
                print(string_length)
                for letter in instance:
                    if letter == ' ':
                        print(letter_count)

                        if(letter_count == 0):
                            print("inbefore-" + instance + "-")
                            instance = instance.lstrip()
                            print("inafter-" + instance + "-")
                            start = start + 1
                            string_length = string_length = 1
                        
                        elif(letter_count == string_length - 1):
                            print("before-" + instance + "-")
                            instance = instance.rstrip()
                            print("after-" + instance + "-")
                            end = end - 1
                    
                    letter_count += 1
                
                print("-" + instance + "-")
                print(end)
                print(start)
                print()
                # -------------------------------------------------
                

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



