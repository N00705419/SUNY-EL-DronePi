import sqlite3

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

def application(env, start_response):
    start_response('200 OK', [('Content-Type','text/html')])

    connection = sqlite3.connect("../www/database/pi_database.db")
    connection.row_factory = dict_factory

    cursor = connection.cursor()

    cursor.execute("SELECT * FROM images DESC")

    results = cursor.fetchall()
    connection.close()

    return results