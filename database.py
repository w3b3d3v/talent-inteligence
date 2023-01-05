import sqlite3
from sqlite3 import Error

class Database:
    def __init__(self, db_file) -> None:
        self.db_file = db_file
    
    def __str__(self) -> str:
        return str(self.db_file)

    def create_connection(self):
        try:
            conn = sqlite3.connect(self.db_file)
            return conn
        except Error as e:
            print(e)
            return

def create_predictions_table(self, conn):
    table_sql = """CREATE TABLE IF NOT EXISTS predictions (id integer PRIMARY KEY, user_id integer NOT NULL UNIQUE, job text, techs text);"""
    if not conn:
        return False
    try:
        c = conn.cursor()
        c.execute(table_sql)
        return True
    except Error as e:
        print(e)
        return False

def insert_prediction(self, conn, prediction):
    insert_sql = """INSERT INTO predictions (user_id, job, techs) VALUES (?, ?, ?);"""
    
    try:
        c = conn.cursor()
        c.execute(insert_sql, prediction)
        c.commit()
        return c.lastrowid

    except Error as e:
        print(e)
        return False