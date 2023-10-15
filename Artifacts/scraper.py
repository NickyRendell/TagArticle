import requests
from bs4 import BeautifulSoup

def get_article_text(url):
    # Make an HTTP request to the given URL
    response = requests.get(url)
    
    # If the request was successful, parse the content using BeautifulSoup
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extract the specific div containing the article content
        content_div = soup.find('div', class_='article')
        
        # If the div is found, extract paragraphs from it
        if content_div:
            paragraphs = content_div.find_all('p')
            
            # Join the paragraphs and return the text
            article_text = ' '.join([p.get_text() for p in paragraphs])
            return article_text
        else:
            print("Error: Article content not found.")
            return None

    else:
        print(f"Error {response.status_code}: Unable to fetch the article.")
        return None
