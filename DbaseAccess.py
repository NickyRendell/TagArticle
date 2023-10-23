import requests
import re
import json

def clean_html(raw_html):
    """Function to clean HTML tags from a string."""
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    return cleantext

def get_wp_posts(page=1, endpoint="https://cphpost.dk/wp-json/wp/v2/posts", fields="id,title,excerpt", per_page=10):
    all_posts = []

    url = f"{endpoint}?_fields={fields}&per_page={per_page}&page={page}"
    response = requests.get(url)
    
    # Check if the request was successful
    if response.status_code != 200:
        print(f"Request failed with status code: {response.status_code}")
        return None

    posts = response.json()
    
    for post in posts:
        post_id = post.get('id')
        title = post.get('title', {}).get('rendered', '')
        excerpt = post.get('excerpt', {}).get('rendered', '')
        excerpt = clean_html(excerpt).split('\n\n')[0]  # Clean HTML tags and get content up to the first two newlines
        
        all_posts.append({
            'id': post_id,
            'title': title,
            'excerpt': excerpt
        })

    return all_posts

# Example usage
page_number = 1
posts = get_wp_posts(page=page_number, per_page=5)
if posts is not None:
    for post in posts:
        print(json.dumps(post, indent=2))
