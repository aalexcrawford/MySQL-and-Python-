#!/usr/bin/python

import mysql.connector

def connect():
    conn = mysql.connector.connect(
        host="incognito-db.cldmcuhzf49p.us-east-2.rds.amazonaws.com",
        database="InCognito",
        user="API",
        password="G3n3r1cP@ssw0rd!"
    )

    return conn

def showDatabases():
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("SHOW DATABASES")
    rows = cursor.fetchall()
    for row in rows:
        print(row)
    return cursor.rowcount

    
