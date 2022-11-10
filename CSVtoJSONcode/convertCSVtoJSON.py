# modified code from https://www.askpython.com/python/examples/convert-csv-to-json
import csv
import json

# Takes the Mechanical Turk csv output file and creates a basic JSON for later tag extraction
 
def csv_to_json(csv_file_path, json_file_path):
    data_dict = {}
 
    with open(csv_file_path, encoding = 'utf-8') as csv_file_handler:
        csv_reader = csv.DictReader(csv_file_handler)
 
        count = 0
 
        for rows in csv_reader:
 
            key = rows['AssignmentId'] # uses the MT assignment id as the json key

            data_dict[key] = rows

            count+=1
            
    with open(json_file_path, 'w', encoding = 'utf-8') as json_file_handler:
        json_file_handler.write(json.dumps(data_dict, indent = 4))
# ----------------------------------------------------------------------------------

# csv_file_path = input('Enter the absolute path of the CSV file: ')
csv_file_path = 'Batch_MT_results_combined_amp_removed.csv'
# json_file_path = input('Enter the absolute path of the JSON file: ')
json_file_path = 'mt_combined.json'
 
csv_to_json(csv_file_path, json_file_path)

