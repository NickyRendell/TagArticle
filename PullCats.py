

def extract_categories_from_text(text):
    categories = ["politics", "business", "technology", "health", "entertainment", 
                  "sports", "science", "travel", "culture", "lifestyle", "education"]
    
    for category in categories:
        if category.lower() in text.lower():
            return category    
    return None


def extract_category(text):
    categories = [
        "Information Providing", 
        "Opinion/Analysis", 
        "Entertainment", 
        "Inspirational/Motivational", 
        "Educational/Instructional", 
        "Persuasive/Argumentative", 
        "Narrative/Storytelling", 
        "Interview/Profile", 
        "Review/Critique", 
        "Investigative/Exposé"
    ]
    
    for category in categories:
        if category.lower() in text.lower():
            return category
    return None

def extract_sentiment(text):
    sentiments = ["Positive", "Neutral", "Negative"]
    
    for sentiment in sentiments:
        if sentiment.lower() in text.lower():
            return sentiment
    return None


def extract_target_audience(text):
    target_audiences = ["General", "Professionals", "Youth/Teens", "Seniors", "Parents", "Academics"]
    
    for audience in target_audiences:
        if audience.lower() in text.lower():
            return audience
    return None

def extract_region(text):
    regions = ["Local", "National", "International"]
    
    for region in regions:
        if region.lower() in text.lower():
            return region
    return None


def extract_user_needs(text):
    user_needs = ["Update me", "Educate me", "Give me an advantage", "Connect me", "Inspire me", "Entertain me"]
    
    for user_need in user_needs:
        if user_need.lower() in text.lower():
            return user_need
    return None