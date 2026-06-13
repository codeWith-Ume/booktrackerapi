import mysql.connector

def get_connection():
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="1",
        database="bookdb"
    )
    
    return connection