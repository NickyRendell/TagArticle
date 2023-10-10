import os
import openai
from dotenv import load_dotenv

# Specify the path to the .env file
#This is the laptop path
#env_path = r'C:\Remote\DC.RandD\Ontology\OntCreate\OntologyCreation\config\.env'

#PC path
#env_path = r'C:\Users\charl\Dropbox\Dev\DC.RandD\Ontology\OntCreate\OntologyCreation\config\.env'
#laptop path
env_path = r'C:\Remote\Article\ArticleCheck\config\.env'


# Load the .env file
load_dotenv(dotenv_path=env_path)

org_id = os.getenv('OPENAI_ORG_ID')
openai.api_key = os.getenv('OPENAI_API_KEY')

#user input the text to be categorised
text = input("Please enter the text to be categorised: ")

EngUserNeeds = """Update me : Tells the reader about something that just happened or came to light. \
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
                    Stories that hit the reader in the heart and diaphragm and may cause a lump in the throat. Often about a person who is or has been in a challenging situation. Looking back in time. Does not focus on solutions and role models. \
Inspire me: Gives the reader a sense of empowerment and/or curiosity. Can be about other people, companies or organizations that have achieved something big against all odds, or about a possible solution to a big problem.\
    Solution journalism. Highlights role models the reader can aspire to.Inspires the reader to think in new ways and strive for something bigger. \
        Gives hope. Provides input to look at problems, challenges, situations in a different and more constructive way. \n
        Entertain me: Puts a smile on the reader's face. Lies in its tone and angle up to entertain the user. Typically not newsworthy or materialistic. \
          Provides a respite where the reader can take their mind away from their own and the world's problems. Distracts your mind with something fun, exciting, interesting, fascinating or entertaining."""


content = "###Categorise Article into User Needs###\n{EngUserNeeds}\n\n###Instructions###\nCategorise the following article into one of the six user needs described above.\n{text}\n"

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
               "description": "The predicted areas of learning."
           }
       },
       "required": [
           "prediction"
       ]
   }
}


r = openai.ChatCompletion.create(
   model="gpt-4",
   temperature=0.0,
   messages=[{"role": "user", "content": content}],
   functions=[function],
   function_call={"name": "predict_area_of_learning"},
)