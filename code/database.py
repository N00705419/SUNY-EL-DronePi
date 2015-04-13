#!/usr/bin/python
import sqlite3
import os

dir_path = os.path.dirname(os.path.abspath(__file__))

class Database:

    def __init__(self, path_to_database):
        self.conn = sqlite3.connect(os.path.join(dir_path, path_to_database))
        self.cur = self.conn.cursor()

    def tableCreate(self, ):
        self.cur.execute("CREATE TABLE images(dateTime TEXT, path_to_image TEXT, latitude TEXT, longitude TEXT, altitude TEXT) ")

    # receives an the data object with format: data = { 'dateTime': '', 'pathToImage': '', 'latitude': '', 'longitude': '', 'altitude': '' } and saves it to the database
    def dataEntry(self, data):
        with self.conn:
            self.cur.execute("INSERT INTO images (dateTime, path_to_image, latitude, longitude, altitude) VALUES( ?, ?, ?, ?, ?)", (data['dateTime'], data['pathToImage'], data['latitude'], data['longitude'], data['altitude']))
            self.conn.commit()
            # print("Data successfully recorded in the database")
            # os.system( "echo 'data saved in the database' >> log.txt" )
