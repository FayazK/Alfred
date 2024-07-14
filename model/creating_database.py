from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import uuid
import sqlite3 as sql
import pandas as pd

class database:
    path = None
    def set_path(self,path):
        database.path = path
    def get_path(self):
        return self.path
    
    def upload_data(self, assistant_id, collection_id):
        name = self.path.split('/')[-1]
        UUid = str(uuid.uuid4())
        with sql.connect("database.db") as con:
            cur = con.cursor()

            cur.execute('''INSERT INTO files (uuid, name, assistant_id, collection_id) 
                VALUES (?, ?, ?, ?)''',
                (UUid, name, assistant_id, collection_id) )
            con.commit()
            print("Record successfully added")
        con.close()

    def update_assistant_data(assistant_id,uuid):
        with sql.connect("database.db") as con:
            cur = con.cursor()
            cur.execute('''UPDATE files
                           SET assistant_id = ?
                           WHERE uuid = ?''',
                        (assistant_id, uuid))
            con.commit()
            print("Record successfully updated")
        con.close()

    def insert_rows(self):
        data = pd.read_excel(self.path,skiprows=1)
        data = data.drop(['Voids', '% AC', 'Avg. RRI', 'Avg. SIP','Avg. Rut Depth', 'Specimen'], axis = 1)
        data = data.dropna(subset=['Company/\nProject']).iloc[:-1,]
        conn = sqlite3.connect('database.db')
        cur = conn.cursor()
    
        for index, row in data.iterrows():
            batt_id = row['BATT ID']
            cmpy_name = row['Company/\nProject']
            detail = row['Details']
            mix = row['Mix Type']
            binder_pg = row['Binder PG']
            binder_cnt = row['Binder Content']
            nmas = row['NMAS']
            rap = row['RAP %']
            fiber = row['Fiber']
            dosage = row['Dosage']
            additive1 = row['Additive #1']
            dosage1 = row['Dosage #1']
            spaciment_id = row['Specimen ID']
            ct = row['Corr. \nAvg. CT']
            cur.execute('''INSERT INTO records (
                        BATT_ID,
                        Project,
                        Details,
                        MixType,
                        Binder_PG,
                        Binder_Content,
                        NMAS,
                        RAP,
                        Fiber,
                        Dosage,
                        Additive,
                        Dosage1,
                        Specimen_ID,
                        CT_index
                    ) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', (
                        batt_id,
                        cmpy_name,
                        detail,
                        mix,
                        binder_pg,
                        binder_cnt,
                        nmas,
                        rap,
                        fiber,
                        dosage,
                        additive1,
                        dosage1,
                        spaciment_id,
                        ct,
                ))
            conn.commit()
            print('successfully inserted all records')

    def create_file_table(self):
        conn = sqlite3.connect('database.db')
        cur = conn.cursor()
        conn.execute('''CREATE TABLE IF NOT EXISTS files (
                    uuid TEXT PRIMARY KEY,
                    name TEXT,
                    assistant_id TEXT,
                    collection_id TEXT,
                    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )''')
        conn.close()
    def create_record_table(self):
        conn = sqlite3.connect('database.db')
        cur = conn.cursor()
        conn.execute('''CREATE TABLE IF NOT EXISTS records (
                    BATT_ID TEXT,
                    Project TEXT,
                    Details TEXT,
                    MixType TEXT,
                    Binder_PG TEXT,
                    Binder_Content  INTEGER,
                    NMAS TEXT,
                    RAP	 TEXT,
                    Fiber TEXT,
                    Dosage TEXT,
                    Additive  TEXT,
                    Dosage1 TEXT,  
                    Specimen_ID TEXT,
                    CT_index INTEGER
                )''')
        conn.close()



