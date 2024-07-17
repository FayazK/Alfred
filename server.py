from flask import Flask, request, jsonify, redirect, url_for
from model.assistant import chat_creation, chat_with_assitant
from flask_cors import CORS
import os
import pandas as pd
import sqlite3 as sql
import taskingai
from model.custom_assistant import create_or_fetch_assistant, create_assistant_only
from model.creating_database import database
from dotenv import load_dotenv
import logging

logging.basicConfig(level=logging.DEBUG)
#X5lMGRxmL4ML018K9Kh11nC6
def convert_excel_to_html(excel_path, html_path):
    df = pd.read_excel(excel_path)
    df.to_html(html_path)
    
app = Flask(__name__)
CORS(app) 

load_dotenv()


T_API_KEY = os.getenv('Tasking_API_KEY')
taskingai.init(api_key=T_API_KEY,host='https://tasking.fayazk.com')

UPLOAD_FOLDER = 'data'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

#To fetch all the assistants records from database
def show_records():
    '''The function will return the list of all the assistant present in database to show in card layout'''
    data = []
    with sql.connect("database.db") as con:
        cur = con.cursor()
        records = cur.execute('''SELECT * FROM files''')
        count = 1
        for record in records:
            data.append({'name': record[1], 'date': record[4], 'image': 'static/chat.png','link': f'{record[0]}','key': count,'type':'chat'}) #the link contian UUID of the file
            count += 1
        con.commit()
    con.close()
    return data

def File_Upload(file_name):
    '''Handle upload file request creating assistant, inserting into the databse'''
    file = file_name
    if file.name == '':
        return {"message": "No selected file",'code':'404'}
    if file:
        convert_excel_to_html(f"./{UPLOAD_FOLDER}/{file.name}", "./data/output2.html")
        assistant_id, collection_id = create_or_fetch_assistant(f"./{UPLOAD_FOLDER}/output2.html")
        datab = database()
        datab.set_path(f"./{UPLOAD_FOLDER}/{file.name}")
        datab.upload_data(assistant_id,collection_id)
        datab.insert_rows() #insert all the records in a file
        return {"message": "File uploaded successfully",'code':'200', "filename": file.name}

@app.route("/create_assistant",  methods=['GET','POST'])
def create_assistant():
    '''create assistant if deleted'''
    value = request.args.get('value')
    uuid = request.args.get('uuid')
    if request.method == 'POST': 
        if value:
           assistant_id, collection_id = create_assistant_only(collection_id=value)
           datab = database()
           datab.update_assistant_data(assistant_id,uuid)
    else:
        # Handle GET request if needed
        return jsonify({"message": "Please upload a file", "value": value}), 200


def index(uuid,u_input, chat_id):
    '''main endpoing it will hadle the chat conversation with assitatn based on UUID'''
    
    try:
        u_input = u_input
        chat_id = chat_id
        with sql.connect("database.db") as con:
            cur = con.cursor()
            records = cur.execute('''SELECT * FROM files WHERE uuid = ?''', (uuid,))
            record = records.fetchone()
            assistant_id = record[2]
        if not chat_id:
            try:
                chat = chat_creation(assistant_id=assistant_id)
                chat_id = chat.chat_id
            except taskingai.client.rest.ApiException as e:
                value = record[3]
                uuid = record[0]
                return  {'message':"Error while while creating chat id Assistant does not exist."} # Redirect to create_assistant
                    
        if u_input:
            u_input = f'''{u_input}
                        uuid = {uuid} "use uuid only when accessing API/database".'''
            print(u_input)
            response = chat_with_assitant(chat_id=chat_id, assist_id=assistant_id, u_input=u_input)
            print('chat gpt response', response.content.text)
            return {'message': response.content.text, 'uuid': uuid, 'chat_id': chat_id}
            
        else:
            return {'message': 'No message provided'}
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        return {'message': 'Unexpected error occurred'}


