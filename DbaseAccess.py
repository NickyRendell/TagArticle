import requests
import re
import codecs
from bs4 import BeautifulSoup

# # Define the API endpoint for the second page with the specific fields
# api_endpoint = "https://cphpost.dk/wp-json/wp/v2/posts?per_page=2&_fields=id,title,excerpt"

# # Make a GET request to the API
# response = requests.get(api_endpoint)

# # Check if the request was successful (status code 200)
# if response.status_code == 200:
#     # Get the response text as a string
#     response_text = response.text

#     print(response_text)

#     # Find the index of '<div class="woocommerce">'
#     woocommerce_index = response_text.find(r'<div class=\"woocommerce\">')

#     if woocommerce_index != -1:
#         # Chop off the text at and including '<div class="woocommerce">'
#         cleaned_response_text = response_text[:woocommerce_index]

#         # Remove invalid escape sequences from the response text
#         cleaned_response_text = re.sub(r'\\[^\\"/bfnrtu]', '', cleaned_response_text)

#         # Extract the raw id, title, and excerpt
#         raw_id_index = cleaned_response_text.find('"id":')
#         raw_title_index = cleaned_response_text.find('"title":{"rendered":"')
#         raw_excerpt_index = cleaned_response_text.find('"excerpt":{"rendered":"')

#         if raw_id_index != -1 and raw_title_index != -1 and raw_excerpt_index != -1:
#             raw_id_match = re.search(r'\d+', cleaned_response_text[raw_id_index + 6:raw_title_index])
#             raw_id = raw_id_match.group(0) if raw_id_match else 'Number not found'
#             raw_title = cleaned_response_text[raw_title_index + len('"title":{"rendered":"'):raw_excerpt_index].strip(', \t\n\r')
#             raw_excerpt = cleaned_response_text[raw_excerpt_index + len('"excerpt":{"rendered":"'):]
#             raw_excerpt = raw_excerpt[:raw_excerpt.find('"')].strip(', \t\n\r')

#             # Decode the raw title to remove Unicode escape sequences
#             cleaned_title = codecs.decode(raw_title, 'unicode_escape')

#             # Clean up the excerpt by removing HTML tags
#             soup = BeautifulSoup(raw_excerpt, 'html.parser')
#             cleaned_excerpt = soup.get_text()

#             #Print the extracted information
#             print("Raw ID:", raw_id)
#             print("Cleaned Title:", cleaned_title)
#             print("Cleaned Excerpt:", cleaned_excerpt)
#         else:
#             print("Required information not found in the response.")
#     else:
#         print("'<div class=\"woocommerce\">' not found in the response.")
# else:
#     print("Failed to retrieve data. Status code:", response.status_code)


# Define the API endpoint for the second page with the specific fields
api_endpoint = "https://cphpost.dk/wp-json/wp/v2/posts?per_page=10&_fields=id,title,excerpt"

# Make a GET request to the API
response = requests.get(api_endpoint)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Get the response text as a string
    response_text = response.text

    print(response_text)

    pattern = re.compile(r'\{"id":(\d+),"title":\{"rendered":"(.*?)"\},"excerpt":\{"rendered":"(.*?)"\}(,"protected":false)?\}')
    matches = pattern.findall(response_text)

# Extracting and printing the id, title, and excerpt for each match
    for match in matches:
        id, title, excerpt, _ = match
        print(f'ID: {id}\nTitle: {title}\nExcerpt: {excerpt}\n{"-"*50}')