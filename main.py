import os
import openai
from dotenv import load_dotenv
from NewScraperTest import get_article_text
import json
#from scraper import get_article_text

# Specify the path to the .env file
#This is the laptop path
#env_path = r'C:\Remote\DC.RandD\Ontology\OntCreate\OntologyCreation\config\.env'

def categorise_url(domain):

    #PC path
    #env_path = r'C:\Users\charl\Dropbox\Dev\article\TagArticle\config\.env'
    #laptop path
    #env_path = r'C:\Remote\Article\ArticleCheck\config\.env'

    results = {}

    # Load the .env file
    #load_dotenv(dotenv_path=env_path)

    #org_id = os.getenv('OPENAI_ORG_ID')
    openai.api_key = os.environ.get('OPENAI_API_KEY')

    ArticleText, Restricted = get_article_text(domain)

    results['Is article restricted?'] = Restricted

    ArticleText = str(ArticleText)

    ArticleText = ' '.join(ArticleText.split())

    print(ArticleText)

    #text = "Marko’s ambiguous comments about Pérez’s future in the team have ignited a flurry of speculation in the racing world. He suggested that the decision now rests solely with Pérez, adding that Red Bull currently has no alternatives. This statement follows Pérez’s less-than-stellar performance at the Qatar Grand Prix, where he qualified 13th and was embroiled in a three-car collision during the sprint race."

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


    content = f"###Categorise Article accoring to user needs###\n{EngUserNeeds}\n\n###Instructions###\nYou are a newspaper editor, given the above descriptions of the different user needs categories, return just one of categories that best applies to the following text: \n{ArticleText}\n"


    function = {
        #We will change the payload as needed
    "name": "predict_user_need",
    "description": "Article categorisation into user needs.",
    "parameters": {
        "type": "object",
        "properties": {
            "prediction": {
                "type": "array",
                "items": {
                    "type": "string",
                    "enum": [
                        "Update me",
                        "Educate me",
                        "Give me an advantage",
                        "Connect me",
                        "Inspire me",
                        "Entertain me",
                        "None"
                    ]
                },
                "description": "Predicting user needs."
            }
        },
        "required": [
            "prediction"
        ]
    }
    }


    r = openai.ChatCompletion.create(
    model="gpt-4",
    temperature=0.3,
    messages=[{"role": "user", "content": content}],
    functions=[function],
    function_call={"name": "predict_user_need"},
    )


    results["User Need"] = json.loads(r["choices"][0]["message"]["function_call"]["arguments"])["prediction"]
    print(results)
    return results


    