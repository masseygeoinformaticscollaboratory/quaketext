import csv
import json

include_empty_tweets = False

# -------------------------------------------------------------------------
light_tag_json_file_path = "common-200.json" 
csv_file_path = "iaa_results.csv" 

if(include_empty_tweets == True):
    csv_file_path = "light_tag_results_all_tweets.csv" 

# light_tag_csv_file = open(csv_file_path, 'w', encoding = 'utf-8')
# light_tag_csv_file.write('AssignmentStatus' + "\t" + 'tweetId' + "\t" + 'num taggers' + "\t" + 'label' + "\t" + 'instance' +"\t" + 'start' +"\t" + 'end' +"\t" + 'tweetText' + "\n")
 
#  read in input json and output data to light_tag_results.csv
with open(light_tag_json_file_path, encoding = 'utf-8') as json_file_handler:
    
    data = json.load(json_file_handler)

    count = 0
    tc = 0
    sophie_count = 0
    sami_count = 0
    true_neg = 0
    true_pos = 0
    false_neg = 0
    false_pos = 0

    # https://stackoverflow.com/questions/41445573/python-loop-through-json-file
    for i in data['examples']:
        count +=1
        current_tweet = i['content']
        true_neg += len(current_tweet.split())
        # print(len(current_tweet.split()))
        # print(len("tweet".split()))
        # print(i['content'])

        for annotation in i['annotations']:
            # print (annotation['correct'])
            if annotation['correct'] == True or annotation['correct'] == None or annotation['correct'] == False:
                print (annotation['correct'])
                current_value = str(annotation['value'])
                value_word_count = len(current_value.split())
                sophie_tag = False
                sami_tag = False
                for person in annotation['annotated_by']:
                    
                        if person['annotator_id'] == 2:
                            # print (person)
                            # print (current_value)
                            # print(value_word_count)
                            sophie_count +=1
                            sophie_tag = True
                        elif person['annotator_id'] == 3:
                            # print (person)
                            # print (current_value)
                            # print(value_word_count)
                            sami_count +=1
                            sami_tag = True
                
                if sami_tag == True and sophie_tag == True:
                    true_neg -= value_word_count
                    true_pos += value_word_count
                elif sami_tag == True and sophie_tag == False:
                    true_neg -= value_word_count
                    false_neg += value_word_count
                elif sami_tag == False and sophie_tag == True:
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

    print(sophie_count)
    print(sami_count)
    print("count", count)

