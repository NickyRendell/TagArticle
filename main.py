import semantic_kernel as sk
from semantic_kernel.connectors.ai.open_ai import AzureTextCompletion, OpenAITextCompletion
from dotenv import load_dotenv
from scraper import get_article_text
from PullCats import extract_categories_from_text, extract_category, extract_sentiment, extract_target_audience, extract_region
import os

# Specify the path to the .env file
#This is the laptop path
#env_path = r'C:\Remote\DC.RandD\Ontology\OntCreate\OntologyCreation\config\.env'

#PC path
#env_path = r'C:\Users\charl\Dropbox\Dev\DC.RandD\Ontology\OntCreate\OntologyCreation\config\.env'
#laptop path
env_path = r'C:\Remote\DC.RandD\Ontology\OntCreate\OntologyCreation\config\.env'


# Load the .env file
load_dotenv(dotenv_path=env_path)
 

def categorise_url(domain):

    #Initialize the SK
    deployment = os.getenv('AZURE_OPENAI_DEPLOYMENT_NAME')
    endpoint = os.getenv('AZURE_OPENAI_ENDPOINT')
    api_key = os.getenv('AZURE_OPENAI_KEY')
    
    #deployment = os.getenv('GPT4_ENGINE')
    #endpoint = os.getenv('GPT4_BASE_URL') 
    
        # Configure AI service used by the kernel

    useAzureOpenAI = True

    #Initialise
    kernel = sk.Kernel()

    if useAzureOpenAI:
        kernel.add_text_completion_service("dv", AzureTextCompletion(deployment, endpoint, api_key))
    else:
        api_key, org_id = sk.openai_settings_from_dot_env()
        kernel.add_text_completion_service("dv", OpenAITextCompletion("text-davinci-003", api_key, org_id))


    #set up a dict to store the results
    results = {}

    ArticleText = str(get_article_text(domain))

    context = kernel.create_new_context()

    context["history"] = ""

    firstPrompt = """You are a newspaper editor. Tasked with categorising the articles that your staff create. {{$history}} {{$userInput}}}"""  

    summarize = kernel.create_semantic_function(firstPrompt, max_tokens= 1000, temperature=0.1, top_p=0.1)

    context["userInput"] = "Please examine the following and return how you think it should categorised out of the following categories: Politics, Business, Technology, Health, Entertainment, Sports, Science, Travel, Culture, Lifestyle, Education. Here is the article: " + ArticleText

    bot_answer = (summarize(context=context))

    context["history"] += f"\nUser: {context['userInput']}\nChatBot: {bot_answer}\n"

    CatSearch = extract_categories_from_text(str(bot_answer))

    #add the results to the dict
    results["Category"] = CatSearch

    context["userInput"] = "Excellent, now categorise the article in terms of whether the article is one of the following: Information Providing, Opinion/Analysis, Entertainment, Inspirational/Motivational, Educational/Instructional, Persuasive/Argumentative, Narrative/Storytelling, Interview/Profile, Review/Critique, Investigative/Exposé"

    bot_answer = summarize(context=context)

    context["history"] += f"\nUser: {context['userInput']}\nChatBot: {bot_answer}\n"

    CatSearch = extract_category(str(bot_answer))

    #add the results to the dict
    results["Type"] = CatSearch

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

