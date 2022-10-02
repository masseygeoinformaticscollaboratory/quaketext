# https://www.askpython.com/python/examples/convert-csv-to-json
import csv
import json
 
def csv_to_json(csv_file_path, json_file_path):
    #create a dictionary
    data_dict = {}
 
    #Step 2
    #open a csv file handler
    with open(csv_file_path, encoding = 'utf-8') as csv_file_handler:
        csv_reader = csv.DictReader(csv_file_handler)
 
        #convert each row into a dictionary
        #and add the converted data to the data_variable
 
        count = 0
 
        for rows in csv_reader:
 
            #assuming a column named 'No'
            #to be the primary key
            # try:
            #     json_object = json.loads(rows['Answer.taskAnswers'])
            # except:
            #     print("count %d" % count)
            #     for i in json_object['entities']:
            #         print(i)
            #     # print(json_object.entities)
            #     print("\n")
            
            key = rows['AssignmentId']

            # rows = json_object

            data_dict[key] = rows

            # json_object = json.loads(rows['Answer.taskAnswers'])
            # data_dict[key] = json_object

            # if count < 2:
            #     # json_object = json.loads(rows['Answer.taskAnswers'])
            #     # print("row= %s" % json_object)
            #     print("\n")
            #     # print("data_dict[key]= %s" % data_dict[key])
            #     print("\n")
            #     print("Answer.taskAnswers= %s" % rows['Answer.taskAnswers'])
                

            count+=1
            

 
    #open a json file handler and use json.dumps
    #method to dump the data
    #Step 3
    with open(json_file_path, 'w', encoding = 'utf-8') as json_file_handler:
        #Step 4
        json_file_handler.write(json.dumps(data_dict, indent = 4))
# ----------------------------------------------------------------------------------


# file names
csv_file_path = input('Enter the absolute path of the CSV file: ')
# Batch_MT_results_combined_amp_removed.csv
json_file_path = input('Enter the absolute path of the JSON file: ')
# mt_combined.json
 
csv_to_json(csv_file_path, json_file_path)

