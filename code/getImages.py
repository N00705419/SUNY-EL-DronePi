import sqlite3
import json


def get_my_jsonified_data():
    with sqlite3.connect('../www/database/pi_database.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM images;")
        data = cursor.fetchall()
        return json.dumps(data)

def application(env, start_response):
    start_response('200 OK', [('Content-Type','text/html')])
    return get_my_jsonified_data()