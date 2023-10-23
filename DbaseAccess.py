import requests
import pandas as pd
import json
import re

def clean_html(raw_html):
    """Function to clean HTML tags from a string."""
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    return cleantext

def get_wp_posts(endpoint="https://cphpost.dk/wp-json/wp/v2/posts", fields="id,excerpt,title", per_page=1):
    page = 1
    all_posts = []

    while True:
        url = f"{endpoint}?_fields={fields}&per_page={per_page}&page={page}"
        response = requests.get(url)

        if response.status_code == 200:
            try:
                posts = response.json()
            except json.JSONDecodeError:
                print("The response is not in JSON format.")
                print("Response text:", response.text)
                break
            
            if not posts:
                break  # Exit the loop if no more posts are returned

            for post in posts:
                raw_title = post.get("title", {}).get("rendered", "")
                raw_excerpt = post.get("excerpt", {}).get("rendered", "")

                clean_title = clean_html(raw_title).strip()
                clean_excerpt = clean_html(raw_excerpt).strip().split("\n\n")[0]

                extracted_data = {
                    "id": post.get("id"),
                    "title": clean_title,
                    "excerpt": clean_excerpt
                }
                all_posts.append(extracted_data)

            page += 1  # Go to the next page
        else:
            print(f"Failed to retrieve posts. HTTP Status Code: {response.status_code}")
            print("Response text:", response.text)
            break

    df_posts = pd.DataFrame(all_posts)
    return df_posts

# Example usage
df_posts = get_wp_posts()
if not df_posts.empty:
    print(df_posts)
