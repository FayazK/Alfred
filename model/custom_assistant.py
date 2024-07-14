from model.helper_functions import Assistant
from dotenv import load_dotenv
import os

load_dotenv()
embd_model_id = os.getenv('embed_model_id')
model_id = os.getenv('model_id') 
def create_or_fetch_assistant(path, assistant_id = None):  
    if assistant_id:
        #assistant exist only edit the assistant
        custom_assistant = Assistant()
        custom_assistant.set_assistant_id(assistant_id)
        collection = custom_assistant.Create_collection(name="Projects records latest",embd_model_id = embd_model_id) #avoid using duplicate actions
        custom_assistant.Create_insert_records(path, collection.collection_id, title="Asphalt prjects records latest")
        custom_assistant.Edit_assistant(custom_assistant.get_assistant_id(), collection.collection_id)
        print(f"Already eixsting assistant with id = {assistant_id} has updated succesfully! ")
    else:
        #assistant does't exist so create one and add knowledge base
        custom_assistant = Assistant()
        assistant = custom_assistant.Create_assistant(model_id=model_id, name="Asphalt mixture expert")
        custom_assistant.set_assistant_id(assistant.assistant_id)
        #collection = custom_assistant.Create_collection(name="Projects records latest",embd_model_id = embd_model_id)
        #collection_id = collection.collection_id
        collection_id = "DbgYm5lrujgwc4b77xthdzf9"
        custom_assistant.Create_insert_records(path, collection_id, title="Asphalt prjects records latest")
        custom_assistant.Edit_assistant(custom_assistant.get_assistant_id(), collection_id)
        #action = custom_assistant.Create_action()
        #action_id = action[0].action_id
        action_id = "bFBdE3D7kzAUhhJc6aZdtSHp"
        print('action id',action_id)
        custom_assistant = custom_assistant.add_action(custom_assistant.get_assistant_id(),action_id)
        print(f'newly created assistant with knowledge base having id = {assistant.assistant_id} succesfully! ')
    return (assistant.assistant_id, collection_id)

def create_assistant_only(collection_id):
    custom_assistant = Assistant()
    assistant = custom_assistant.Create_assistant(model_id=model_id, name="Asphalt mixture expert")
    custom_assistant.Edit_assistant(assistant.assistant_id, collection_id)
    action = custom_assistant.Create_action()
    action_id = action[0].action_id
    print('action id',action_id)
    custom_assistant = custom_assistant.add_action(assistant.assistant_id,action_id)
    return (assistant.assistant_id, collection_id)
