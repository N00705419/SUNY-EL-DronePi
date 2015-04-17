import sqlite3

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


connection = sqlite3.connect("./database/pi_database.db")
connection.row_factory = dict_factory

cursor = connection.cursor()

cursor.execute("SELECT * FROM images DESC")

# fetch all or one we'll go for all.

results = cursor.fetchall()

print results

connection.close()

def application(env, start_response):
    start_response('200 OK', [('Content-Type','text/html')])

    html = "<h1>Hello World From Python</h1>\n"
    html += "<table>\n"
    for k in env:
        html += "<tr><td>{}</td><td>{}</td></tr>\n".format(k, env[k])
    html += "</table>\n"

    return html