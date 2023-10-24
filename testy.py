import requests
import json
from html import unescape

# Define the API endpoint for the second page with the specific fields
api_endpoint = "https://cphpost.dk/wp-json/wp/v2/posts?page=2&_fields=author,id,excerpt,title"

# Make a GET request to the API
response = requests.get(api_endpoint)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Parse the response text as JSON
    response_text = response.text
    error_position = 4294
    print(response_text[error_position-50:error_position+50])

    decoded_text = unescape(response_text)

    try:
        articles = json.loads(decoded_text)
        for article in articles:
            print(article['title']['rendered'])
    except json.JSONDecodeError as e:
        print("Failed to parse response as JSON. Error:", str(e))
    