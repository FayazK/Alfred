import sqlite3 as sql
import taskingai

conn = sql.connect('database.db')

cur = conn.cursor()

cur.execute('DELETE FROM records')

conn.commit()

conn.close()
# ids = ['X5lMxYzfumsV7RiUdDn23795', 'X5lMW7MMhJ1YjcHzsfpnRGsF', 'X5lMa6iPrbwLokpBRzKEXJRp', 'X5lMMY8b5iIB7tsGJaOR1eKc',
# 'X5lMuYTfjxh4A0b9ydjgYuIG', 'X5lMf3JK53jiiEZER46869Dp', 'X5lMc8ce7TZ4eDrPb1TRsTJb', 'X5lMdHA403X1T8gmyYNMQWLE', 'X5lMUyrFVdLKJEfeUF7q7z7Z',
# 'X5lMjRUi9leaeERQag3n04Mf', 'X5lMBTBqzM8QZ3Eq4YvAeQIO', 'X5lMELEswbPfuhHjOhCvLMNa']
# taskingai.init(api_key='tknHZ3g2DVjhO7X33l2MuCtXYaDxcDPa',host='https://tasking.fayazk.com')

# assistants = taskingai.assistant.list_assistants()
# for asistant in assistants:
#     print(asistant.assistant_id)
#     print(asistant)
# for id in ids:
#     taskingai.assistant.delete_assistant(assistant_id=id)