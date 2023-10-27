import re
import requests
import pandas as pd
import json

# Define the API endpoint for the second page with the specific fields
api_endpoint = "https://cphpost.dk/wp-json/wp/v2/posts?per_page=20&_fields=id,title,excerpt"

# Make a GET request to the API
response = requests.get(api_endpoint)

data = response.text

# Split the string into individual records
records = re.split(r'(?=\{"id")', data)

# Remove the first empty string in the list if it exists
if records[0] == '':
    records.pop(0)

# Function to terminate the records
def terminate_record(record):
    # Terminate the record before "protected":false
    if '"protected":false' in record:
        record = record.split('"protected":false')[0]
    # If <div class="woocommerce"> is in the string, terminate the record at that point
    if r"""\t\t""" in record:
        record = record.split(r"""\t\t""")[0]
    return record

# Terminate the records
terminated_records = [terminate_record(record) for record in records]


# Initialize an empty DataFrame
df = pd.DataFrame(columns=["id", "title", "excerpt"])

# Iterate through the records, parse them as JSON, and store the data in the DataFrame
for i, record in enumerate(terminated_records, start=1):
    # Add "}}" to the end of the record string
    record += '"}}'
    
    try:
        # Parse the string as a JSON object
        record_json = json.loads(record)
        
        # Extract the id, title, and excerpt values
        record_id = record_json.get("id", "")
        title = record_json.get("title", {}).get("rendered", "")
        excerpt = record_json.get("excerpt", {}).get("rendered", "")
        
        # Add the data to the DataFrame
        df = df._append({"id": record_id, "title": title, "excerpt": excerpt}, ignore_index=True)
        
        # Print the record
        print(f"Record {i}:\nID: {record_id}\nTitle: {title}\nExcerpt: {excerpt}\n")
    except json.JSONDecodeError as e:
        print(f"Record {i} could not be parsed as JSON: {e}")

# Print the DataFrame
print(df)