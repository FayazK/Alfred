from flask import Flask, request, jsonify, redirect, url_for
from flask_cors import CORS
import sqlite3 as sql
from model import assistant
import os
from dotenv import load_dotenv
import taskingai


app = Flask(__name__)
CORS(app) 

load_dotenv()

T_API_KEY = os.getenv('TASKING_API_KEY')
taskingai.init(api_key=T_API_KEY,host='https://tasking.fayazk.com')


@app.route('/',methods=['GET','POST'])
def home():
    return 'Flask server start working'

#This endpoint is being hit by the assistant to get the records of all the project 
@app.route('/database/<path:uuid>/<path:query>',methods=['GET','POST'])
def query_database(query,uuid):
    '''Thi is api for database it will return all the project based on name of project'''
    data = assistant.extract_sql_query(query,uuid)
    return jsonify(data)

if __name__ == '__main__':
    port = int(os.getenv('FLASK_PORT'))
    flask_host = os.getenv('FLASK_HOST')
    app.run(host=flask_host, port=port)