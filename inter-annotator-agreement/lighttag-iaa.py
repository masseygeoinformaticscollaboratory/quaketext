import csv
import json

include_empty_tweets = False

# -------------------------------------------------------------------------
light_tag_json_file_path = "common-200.json" 
 
with open(light_tag_json_file_path, encoding = 'utf-8') as json_file_handler:
    
    data = json.load(json_file_handler)

    count = 0
    tc = 0
    person1_count = 0
    person2_count = 0
    true_neg = 0
    true_pos = 0
    false_neg = 0
    false_pos = 0

    for i in data['examples']:
        count +=1
        current_tweet = i['content']
        true_neg += len(current_tweet.split())
        # print(len(current_tweet.split()))
        # print(len("tweet".split()))
        # print(i['content'])

        for annotation in i['annotations']:
            # print (annotation['correct'])
            if annotation['correct'] == True or annotation['correct'] == None: # or annotation['correct'] == False:
                print (annotation['correct'])
                current_value = str(annotation['value'])
                value_word_count = len(current_value.split())
                person1_tag = False
                person2_tag = False
                for person in annotation['annotated_by']:
                    
                        # change annotator_ids to change people to compare against
                        if person['annotator_id'] == 2:
                            # print (person)
                            # print (current_value)
                            # print(value_word_count)
                            person1_count +=1
                            person1_tag = True
                        elif person['annotator_id'] == 5:
                            # print (person)
                            # print (current_value)
                            # print(value_word_count)
                            person2_count +=1
                            person2_tag = True
                
                if person2_tag == True and person1_tag == True:
                    true_neg -= value_word_count
                    true_pos += value_word_count
                elif person2_tag == True and person1_tag == False:
                    true_neg -= value_word_count
                    false_neg += value_word_count
                elif person2_tag == False and person1_tag == True:
                    true_neg -= value_word_count
                    false_pos += value_word_count
                        
        
    print("true_neg", true_neg)
    print("false_neg",false_neg)
    print("false_pos",false_pos)
    print("true_pos",true_pos)

    num = true_neg + false_neg + false_pos + true_pos

    observed_agreement = (true_pos + true_neg)/num

    expected_agreement = ((true_pos+false_neg)/num)*((true_pos+false_pos)/num)+ ((true_neg+false_neg)/num)*((true_neg+false_pos)/num)

    kappa = (observed_agreement - expected_agreement) / (1 - expected_agreement)

    print("kappa", kappa)

    print(person1_count)
    print(person2_count)
    print("count", count)

