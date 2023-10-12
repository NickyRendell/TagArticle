import semantic_kernel as sk
from semantic_kernel.connectors.ai.open_ai import AzureTextCompletion
from dotenv import load_dotenv
from scraper import get_article_text
from PullCats import extract_categories_from_text, extract_sentiment, extract_target_audience, extract_region, extract_user_needs
import os

# Specify the path to the .env file
#This is the laptop path
#env_path = r'C:\Remote\DC.RandD\Ontology\OntCreate\OntologyCreation\config\.env'

#PC path
#env_path = r'C:\Users\charl\Dropbox\Dev\DC.RandD\Ontology\OntCreate\OntologyCreation\config\.env'
#laptop path

 

def categorise_url(domain):

    env_path = r'C:\Users\charl\Dropbox\Dev\article\TagArticle\config\.env'


# Load the .env file
    load_dotenv(dotenv_path=env_path)

    #Initialize the SK
    deployment = os.getenv('AZURE_OPENAI_DEPLOYMENT_NAME')
    endpoint = os.getenv('AZURE_OPENAI_ENDPOINT')
    api_key = os.getenv('AZURE_OPENAI_KEY')
    
    #deployment = os.getenv('GPT4_ENGINE')
    #endpoint = os.getenv('GPT4_BASE_URL') 

    # OpenAPI settings
    #api_key = os.getenv('OPENAI_API_KEY')
    #org_id = os.getenv('OPENAI_ORG_ID')


    EngUserNeeds = """These are the descriptions of each user need\n
    Update me : Tells the reader about something that just happened or came to light. \
    Classic news article that states the facts and answers the questions.\
    What happened? Where did this happen? Who is involved? What are the details?\
    This would be centered around a specific incident, event, statement or statement. \
    Representation of case, action and process without a lot of expert opinions or perspectives on other cases.\n
    Educate me : This makes the reader wiser about a topic. Establishes basic knowledge of the subject by explaining concepts, listing chronology, introducing important people, and providing context.\
    The main purpose is to explain something, not to be actionable. Primarily answers questions instead of asking them. Often contains opinions, perspectives and quotes from experts and researchers. As well as quotes or facts from studies, analyzes, reports. Is not the first with the news or breaking news.\n
    Give me an advantage: Helps the reader in their everyday life.\ 
    Concrete advice and guidance that makes a difference for the reader, their company, or their organization. \
    Its main purpose is to enable the reader to act and change something.\
    Contains information to help the reader take action. Critical knowledge so that the reader can make the right choices going forward.\
    Takes the reader by the hand, indicates the steps and identifies a clear solution to their problems.\n
    Connect me: Creates identification with the reader. Describes the experience, course and/or feelings of one or more people.\
    Will always be carried by relatable personal stories that the reader can reflect in and feel seen in.\
    Stories that hit the reader in the heart and diaphragm and may cause a lump in the throat. Often about a person who is or has been in a challenging situation. Looking back in time. Does not focus on solutions and role models. \n
    Inspire me: Gives the reader a sense of empowerment and/or curiosity. Can be about other people, companies or organizations that have achieved something big against all odds, or about a possible solution to a big problem.\
    Solution journalism. Highlights role models the reader can aspire to.Inspires the reader to think in new ways and strive for something bigger. \
    Gives hope. Provides input to look at problems, challenges, situations in a different and more constructive way. \n
    Entertain me: Puts a smile on the reader's face. Lies in its tone and angle up to entertain the user. Typically not newsworthy or materialistic. \
    Provides a respite where the reader can take their mind away from their own and the world's problems. Distracts your mind with something fun, exciting, interesting, fascinating or entertaining."""


    #Initialise
    kernel = sk.Kernel()


    kernel.add_text_completion_service("dv", AzureTextCompletion(deployment, endpoint, api_key))

    #set up a dict to store the results
    results = {}

    ArticleText = str(get_article_text(domain))

    context = kernel.create_new_context()

    context["history"] = ""

    firstPrompt = """You are a newspaper editor. Tasked with categorising the articles that your staff create. {{$history}} {{$userInput}}}"""  

    summarize = kernel.create_semantic_function(firstPrompt, max_tokens= 1000, temperature=0.1, top_p=0.1)

    context["userInput"] = f"""Firstly, based on these descriptions:\n
    {EngUserNeeds}\n

    Categorise the article in terms of whether the article is one of the following: update me, educate me, give me an advantage, connect me, inspire me, entertain me. Here is the article: {ArticleText}"""

    bot_answer = summarize(context=context)

    context["history"] += f"\nUser: {context['userInput']}\nChatBot: {bot_answer}\n"

    CatSearch = extract_user_needs(str(bot_answer))

    #add the results to the dict
    results["User Need"] = CatSearch

    context["userInput"] = "Excellent, now please return how you think it should categorised out of the following categories: Politics, Business, Technology, Health, Entertainment, Sports, Science, Travel, Culture, Lifestyle, Education. Here is the article: " + ArticleText

    bot_answer = (summarize(context=context))

    context["history"] += f"\nUser: {context['userInput']}\nChatBot: {bot_answer}\n"

    CatSearch = extract_categories_from_text(str(bot_answer))

    #add the results to the dict
    results["Category"] = CatSearch

    context["userInput"] = "Now categorise in terms of sentiment: Positive, Neutral, Negative"

    bot_answer = summarize(context=context)

    context["history"] += f"\nUser: {context['userInput']}\nChatBot: {bot_answer}\n"

    CatSearch = extract_sentiment(str(bot_answer))

    #add the results to the dict
    results["Sentiment"] = CatSearch

    context["userInput"] = "Now categorise in terms of audience: General, Professionals, Youth/Teens, Seniors, Parents, Academics"

    bot_answer = summarize(context=context)

    context["history"] += f"\nUser: {context['userInput']}\nChatBot: {bot_answer}\n"

    CatSearch = extract_target_audience(str(bot_answer))

    #add the results to the dict
    results["Target Audience"] = CatSearch

    context["userInput"] = "Finally, given that the article was written in Copenhagen, please categorise the region of the article: Local, National, International"

    bot_answer = summarize(context=context)

    CatSearch = extract_region(str(bot_answer))

    #add the results to the dict
    results["Region"] = CatSearch

    return results

# #print(results)

# print("The article has been categorised as follows: ")
# print("Categories: " + str(results["Categories"]))
# print("TypeCategory: " + str(results["TypeCategory"]))
# print("Sentiment: " + str(results["Sentiment"]))
# print("TargetAudience: " + str(results["TargetAudience"]))
# print("Region: " + str(results["Region"]))

