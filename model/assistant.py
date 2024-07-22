import os
import taskingai
from taskingai.inference import chat_completion, SystemMessage, UserMessage
import sqlite3 as sql
from dotenv import load_dotenv

load_dotenv()
T_API_KEY = os.getenv('TASKING_API_KEY')
taskingai.init(api_key=T_API_KEY,host='https://tasking.fayazk.com')
model_id = os.getenv('MODEL_ID')

def chat_creation(assistant_id):
    chat = taskingai.assistant.create_chat(
    assistant_id = assistant_id)
    return chat
 
def extract_sql_query(query,uuid):
    data = []
    schema = ['uuid','BATT_ID','Project','Details','MixType','Binder_PG','Binder_Content','NMAS','RAP','Fiber','Dosage','Additive','Dosage1','Specimen_ID','CT_index']
    response = chat_completion(
    model_id=model_id,
    messages=[
            SystemMessage(f'You are expert in extracting query from simple plain question. Based on the question: "{query}" and the table schema: {schema} and table name is "records" and the "uuid= {uuid}" generate a sqllite3 query to answer the question. "Your response should return only slite query nothing else"'),
            UserMessage(query),
            ]
        )
    response = response.message.content
    response = response.replace("```sql", "").replace("```", "")
    with sql.connect("database.db") as con:
            cur = con.cursor()
            records = cur.execute(response)
            all_records = records.fetchall()
            for record in all_records:
                json_record = {
                    'retrived from database': record
                }
                data.append(json_record)
            con.commit()
    return data

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
    