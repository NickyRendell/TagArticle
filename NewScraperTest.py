import re
import requests
from bs4 import BeautifulSoup

def get_article_text(url):
    # Make an HTTP request to the given URL
    response = requests.get(url)
    
    # If the request was successful, parse the content using BeautifulSoup
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Check for classes that start with 'article post-' followed by a number
        regex_pattern = r'article post-\d+'
        content_div = soup.find('div', class_=re.compile(regex_pattern))
        
        is_access_restricted = "N"
        
        # If the div is found
        if content_div:
            # Check if 'access-restricted' is in its class
            if 'access-restricted' in content_div['class']:
                is_access_restricted = "Y"
                meta_descriptions = soup.find_all('meta', {'property': 'og:title'})
                if len(meta_descriptions) > 1:
                    return meta_descriptions[1]['content'], is_access_restricted
                else:
                    print("Error: Second meta description not found.")
                    return None, is_access_restricted
            
            # If only the regular div is found, extract paragraphs from it
            else:
                paragraphs = content_div.find_all('p')
                article_text = ' '.join([p.get_text() for p in paragraphs])
                return article_text, is_access_restricted
        else:
            print("Error: Article content not found.")
            return None, is_access_restricted

    else:
        print(f"Error {response.status_code}: Unable to fetch the article.")
        return None, "N"

# Usage
article_content, access_flag = get_article_text("https://cphpost.dk/2023-10-13/news/round-up/new-benefits-rule-for-all-immigrants-need-two-and-a-half-years-full-time-work/")
print(article_content)
print("Is Access Restricted?", access_flag)
