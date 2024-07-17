import taskingai
from taskingai.file import upload_file
import taskingai
from taskingai.retrieval import Record, TokenTextSplitter
from taskingai.retrieval.collection import Collection, create_collection
from taskingai.assistant.memory import AssistantNaiveMemory
from taskingai.assistant import Assistant, AssistantRetrieval, AssistantRetrievalType
from taskingai.assistant import AssistantTool, AssistantToolType
from taskingai.tool import Action
from taskingai.tool import ActionAuthentication, ActionAuthenticationType
from typing import List
from dotenv import load_dotenv 
import os
from model.database_api_schema import DATABASE_API_SCHEMA
load_dotenv()
model_id = os.getenv('model_id')
embed_model_id = os.getenv('embed_model_id')


class Assistant:
    assistant_id = None
    def __init__(self) -> None:
        self.file_path = None
        self.model_id = model_id #Chat compleltion model id
        self.assistant_name =  "Dynamic asphalt engineer"
        self.collection_name = "Asphalt records data"
        self.embed_model_id =  embed_model_id #Embedings model id
        self.collection_id = None
        self.record_title = None #record name or title
        self.DATABASE_API_SCHEMA = DATABASE_API_SCHEMA

    #create assistant with name and model for chat completion
    def Create_assistant(self, model_id, name):
        self.model_id = model_id
        self.assistant_name = name
        print('creating assistant ...')
        sys_prmpt1 = '''You're a civil engineering chatbot equipped with a tabular record of experiments on asphalt mixture, detailing various feature values and the final CT index values. Users can inquire about any feature value for a specific project. Follow user queries precisely, only providing existing data. Never generate records. "Accuracy is key." also "make sure you do not spesify from where to retrive means the database and the files uploaded to you". You can acces data from database and files uploaded to you.
"Use uuid only when user asks for some records otherwise ignore it".'''
        sys_prmpt2 = '''Here are some examples:
            question: when the binder content was 5.25 and binder PG content was PG64-22 in the ATS/REARM HR project what was the CT index value?
            answer: The CT index value for this set of ATS/REARM HR project was 75.2.

            question: when the CT index value was 65 in Hall ACE XP what were the other values?
            answer: For this CT value of "Hall ACE XP" project the Mix type was "RPMLC", binder PG "PG64-22", and binder content "5.6" with a RAP percentage of 20%.
            '''
        sys_prmpt3 = '''if you encounter error while retriving data then print the error in human readable formate with detials of error'''
        sys_prmpt4 = '''###Note
"If your response contains bullet point or table or list or heading return it in HTML format for easy rendering also mimic like a real human"'''
        
        assistant = taskingai.assistant.create_assistant(
            model_id= self.model_id,
            name= self.assistant_name,
            description="You are a civil engineering chatbot that retrieves details about project and its parameters, from the record document uploaded to you based on the user query about a particular project.",
            system_prompt_template=[
                sys_prmpt1,
                sys_prmpt2,
                sys_prmpt3,
                sys_prmpt4
            ],
            memory=AssistantNaiveMemory()
        )
        return assistant
    #Creating collection
    def Create_collection(self, name, embd_model_id):
        self.collection_name = name
        self.embed_model_id = embd_model_id
        print('creating collection ...')
        collection: Collection = create_collection(
            name= self.collection_name,
            description="This is the asphalt mixture records data in a tabular format where each row represents a single project. and the column represents the parameters of the project.",
            embedding_model_id= self.embed_model_id,
            capacity = 1000
        )
        return collection
    
    #Create records
    def Create_insert_records(self, path, collection_id, title = "Mixture records data"):
        self.file_path = path
        self.collection_id = collection_id
        self.record_title = title
        print('creating records ...')
        new_file = taskingai.file.upload_file(file=open(self.file_path, "rb"), purpose="record_file")
        record: Record = taskingai.retrieval.create_record(
            title = self.record_title,
            collection_id=self.collection_id,
            type="file",
            file_id=new_file.file_id,
            text_splitter={"type": "token", "chunk_size": 200, "chunk_overlap": 20},
        )
        return record
    #Edit assistatn if already exit
    def Edit_assistant(self, assistant_id, collection_id):
        self.assistant_id = assistant_id
        self.collection_id = collection_id
        print('editing assistant ...')
        assistant: Assistant = taskingai.assistant.update_assistant(
            assistant_id=self.assistant_id,
            retrievals=[AssistantRetrieval(
                type=AssistantRetrievalType.COLLECTION,
                id=self.collection_id,
            )]
        )
        return 
    
    def Create_action(self):
        actions: List[Action] = taskingai.tool.bulk_create_actions(
            openapi_schema=self.DATABASE_API_SCHEMA,
            authentication=ActionAuthentication(
            type=ActionAuthenticationType.NONE,
            )
        )
        return actions
    
    def add_action(self,assistant_id,action_id):
        assistant: Assistant = taskingai.assistant.update_assistant(
            assistant_id=assistant_id,
            tools=[
                AssistantTool(
                    type=AssistantToolType.ACTION,
                    id=action_id),
            ]
        )
        return assistant
    def set_assistant_id(self, api):
        Assistant.assistant_id = api
    
    def get_assistant_id(self):
        return Assistant.assistant_id 


