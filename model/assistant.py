import os
import taskingai
from dotenv import load_dotenv

load_dotenv()
T_API_KEY = os.getenv('Tasking_API_KEY')
taskingai.init(api_key=T_API_KEY,host='https://tasking.fayazk.com')

def chat_creation(assistant_id):
    chat = taskingai.assistant.create_chat(
    assistant_id = assistant_id)
    return chat
 
# def chat_with_assitant(chat_id, assist_id, u_input):
#     #Create message
#     message = taskingai.assistant.create_message(
#     assistant_id= assist_id,
#     chat_id=chat_id,
#     text=u_input,)
#     #Call the assistant
#     response = taskingai.assistant.generate_message(
#     assistant_id= assist_id,
#     chat_id= chat_id,)
    
#     return response

def chat_with_assitant(chat_id, assist_id, u_input):
    # Create message    
    message = taskingai.assistant.create_message(
            assistant_id=assist_id,
            chat_id=chat_id,
            text=u_input
        )
        
    # Call the assistant to generate a response
    response = taskingai.assistant.generate_message(
            assistant_id=assist_id,
            chat_id=chat_id
        )
    return response
    