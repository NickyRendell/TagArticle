import re
import requests
import pandas as pd
import json
import html
from bench_test import categorise_title_excerpt
import time

# Define the API endpoint for the second page with the specific fields
api_endpoint = "https://cphpost.dk/wp-json/wp/v2/posts?per_page=50&page=1&_fields=id,title,excerpt"

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
        record = record.split('","protected":false')[0]
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
    print (record)  
    
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

def unescape_html_entities(text):
    return html.unescape(text)

df['title'] = df['title'].apply(unescape_html_entities)
df['excerpt'] = df['excerpt'].apply(unescape_html_entities)

# Print the DataFrame

#save to new df
#df.to_csv('CPHPost.csv', index=False)

df.to_csv('filename.csv', encoding='utf-8-sig', index=False)

#create a new column in dataframe called prediction
df['prediction'] = ""

#set up loop that concantenates the title and excerpt with '-' in between then sends the string to the function categorise_title_excerpt
#the function returns a prediction which is then added to the prediction column in the dataframe
for i in range(len(df)):
    title = df['title'][i]
    excerpt = df['excerpt'][i]
    title_excerpt = title + ' - ' + excerpt
    #wait 10 seconds
    time.sleep(10)
    prediction = categorise_title_excerpt(title_excerpt)
    df['prediction'][i] = prediction

#save dataframe to csv with utf-8string
#  encoding
df.to_csv('CPHPostA.csv', encoding='utf-8-sig', index=False)

