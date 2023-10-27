import json

record_string = '''{"id":154583,"title":{"rendered":"Christiania sees huge drop in visitors: \u201cpeople are scared\u201d"},"excerpt":{"rendered":"After recent shootings and gang disturbances, &#8221;people don&#8217;t dare come out here,&#8221; says the manager of culture centre Operaen. Plus, a new study finds AI skills boost your paycheck by 21 percent, and bank home loans boom as mortgages become unattractively expensive."}}'''

# Load the string as a JSON object
record = json.loads(record_string)

# Remove the "rendered" key and assign its value directly to "title" and "excerpt"
record['title'] = record['title']['rendered']
record['excerpt'] = record['excerpt']['rendered']

# Convert the record back to a JSON-formatted string
updated_record_string = json.dumps(record, ensure_ascii=False)
print(updated_record_string)
