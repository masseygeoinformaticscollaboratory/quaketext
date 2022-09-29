import json
import csv

impact_list = ['cancellation','closure','collapse','damage','damaged','dead','death','delay','die','disruption','destroy','destroyed','down','injured','injury','lose','loss','loss of life','malfunction','miss work','missing','no access','obstruction','rescue','stranded','theft','trapped', 'kill']
# missing capitalization of some impact instances
  
# Opening JSON file
f = open('../CSVtoJSONcode/finaltags.json')

test_csv_file = "C:/Users/sophi/Documents/Uni/QuakeText_Project_Files/MT_disaster_impact_input_3.csv"

test_data_dict = {}
# https://stackoverflow.com/questions/17912307/u-ufeff-in-python-string#:~:text=The%20Unicode%20character%20U%2BFEFF,will%20remove%20it%20for%20you.
with open(test_csv_file, "r", encoding = 'utf-8-sig') as csv_file_handler:
    csv_reader = csv.DictReader(csv_file_handler)
 
    count = 0
 
    for rows in csv_reader:
        # print(rows)
 
        key = rows['id']
        # create the dictionary of tweets
        test_data_dict[key] = rows

        count+=1

for tweet in test_data_dict:
    print(test_data_dict[tweet]['text'])
    test_data_dict[tweet]['tag'] = []
    for impact in impact_list:
        if impact in test_data_dict[tweet]['text']:
            print("found impact = " + impact)
            start = test_data_dict[tweet]['text'].find(impact)
            print(start)
            end = test_data_dict[tweet]['text'].rfind(impact)
            print(end)
            current_tags = test_data_dict[tweet]['tag']
            current_tags.extend([{'value':impact,'start':str(start)}])
            test_data_dict[tweet]['tag'] = current_tags
            # test_data_dict[tweet]['tag'] = [{'value':impact,'start':str(start)}]

    
with open("test_result.json", 'w', encoding = 'utf-8') as json_file_handler:
    json_file_handler.write(json.dumps(test_data_dict, indent = 4))


  
# returns JSON object as 
# a dictionary
data = json.load(f)

  
# Iterating through the json
# list

print("hello world")


count = 0
for i in data:
    # print(data[i]['annotations'])
    impact_only_dict = {}
    for anno in data[i]['annotations']:
        if count < 10:
            # print(anno)
            count = count+1

# TODO need to read in tagged data to compare only impact tags
# Read in tweets to see if value list is contained within
# if it is then get start and end and compare with tagged dataset?

    

# Closing file
f.close()