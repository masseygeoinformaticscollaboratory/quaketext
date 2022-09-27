import json
  
# Opening JSON file
f = open('../CSVtoJSONcode/finaltags_lighttag_format.json')
  
# returns JSON object as 
# a dictionary
data = json.load(f)
  
# Iterating through the json
# list

print("hello world")

count = 0
for i in data:
    if count < 10:
        print(i)
    count =+ 1

# Closing file
f.close()