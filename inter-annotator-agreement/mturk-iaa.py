import csv
import json
# top worker ids
WORKER1 = "ATR6RB1RULOC0"
WORKER2 = "A1NF6PELRKACS9"

worker1_dict = []
worker1_count = 0
worker2_dict = []
worker2_count = 0

true_neg = 0
true_pos = 0
false_neg = 0
false_pos = 0

csv_worker_file_path = "../CSVtoJSONcode/all_tags_with_workers.csv"

with open(csv_worker_file_path, 'r', encoding = 'utf-8') as csv_file:
    
    agreement_dict = {}
    final_dict = {}

    csv_reader = csv.DictReader(csv_file, delimiter='\t')

    first = True
    currentId = ""
    currentText = ""
    tagCount = 0
    shared_tweet_count = 0
    worker1found = False
    worker2found = False

    for rows in csv_reader:
        if rows['AssignmentStatus'] == "Approved":
          
            if first == True:
                # if the first row in the file, that is the current
                currentId = rows['Input.id']
                currentText = rows['Input.text']
                true_neg += len(currentText.split())
                first = False    
            elif currentId != rows['Input.id']:
                # if the ids do not match then all the annotations for the previous tweet have been read save to dictionary and change current it and text, and clear annotation list for new tweet 
                currentId = rows['Input.id']
                currentText = rows['Input.text']
                true_neg += len(currentText.split())

                found = False
                if worker1found == True and worker2found == True:
                    shared_tweet_count +=1
                    for item in worker1_dict:
                        # print(item)
                        for compare in worker2_dict:
                            if item == compare:
                                true_pos += len(item['value'].split())
                                true_neg -= len(item['value'].split())
                                found = True
                                compare.update({"compared": "yes"})
                                print(compare)
                        
                        if found == False: #looped through and not in 2
                            false_pos += len(item['value'].split())
                            true_neg -= len(item['value'].split())
                    
                    for item2 in worker2_dict:
                        if item2.get('compared') == None:
                            false_neg += len(item2['value'].split())
                            true_neg -= len(item2['value'].split())


                worker1found = False
                worker2found = False
                worker1_dict = []
                worker2_dict = []
                tagCount = 0

                # print("new id")


            if rows['WorkerId'] == WORKER1 and rows['label'] != '':
                current = worker1_dict
                worker1_count +=1
                worker1_dict = current + [{"label":rows['label'], "value": rows['instance'],"start":rows['startOffset'],"end":rows['endOffset']}]
                worker1found = True

            if rows['WorkerId'] == WORKER2 and rows['label'] != '':
                current = worker2_dict
                worker2_count +=1
                worker2_dict = current + [{"label":rows['label'], "value": rows['instance'],"start":rows['startOffset'],"end":rows['endOffset']}]
                worker2found = True

        tagCount += 1
    
    print ("shared_tweet_count", shared_tweet_count)
  
  
    print("true_neg", true_neg)
    print("false_neg",false_neg)
    print("false_pos",false_pos)
    print("true_pos",true_pos)

    num = true_neg + false_neg + false_pos + true_pos

    observed_agreement = (true_pos + true_neg)/num

    expected_agreement = ((true_pos+false_neg)/num)*((true_pos+false_pos)/num)+ ((true_neg+false_neg)/num)*((true_neg+false_pos)/num)

    kappa = (observed_agreement - expected_agreement) / (1 - expected_agreement)

    print("kappa", kappa)




