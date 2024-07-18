from flask import Flask, request, jsonify, redirect, url_for
from flask_cors import CORS
import sqlite3 as sql
import os
from dotenv import load_dotenv


app = Flask(__name__)
CORS(app) 
load_dotenv()

@app.route('/',methods=['GET','POST'])
def home():
    return 'Flask server start working'

#This endpoint is being hit by the assistant to get the records of all the project 
@app.route('/database/<path:uuid>/<path:name>',methods=['GET','POST'])
def query_database(name,uuid):
    '''Thi is api for database it will return all the project based on name of project'''
    data = []
    print('name = ',name)
    print('uuid = ',uuid)
    with sql.connect("database.db") as con:
        cur = con.cursor()
        records = cur.execute("SELECT * FROM records WHERE Project = ? AND uuid = ?", (name, uuid))
        all_records = records.fetchall()
        #inserting all the records into the database
        for record in all_records:
            json_record = {
            "BATT_ID": record[0],
            "Project": record[1],
            "Details": record[2],
            "MixType": record[3],
            "Binder_PG": record[4],
            "Binder_Content": record[5],
            "NMAS": record[6],
            "RAP": record[7],
            "Fiber": record[8],
            "Dosage": record[9],
            "Additive": record[10],
            "Dosage1": record[11],
            "Specimen_ID": record[12],
            "CT_index": record[13]
            }
            data.append(json_record)
        con.commit()
    return jsonify(data)

if __name__ == '__main__':
    port = int(os.getenv('FLASK_PORT'))
    flask_host = os.getenv('FLASK_HOST')
    app.run(host=flask_host, port=port)