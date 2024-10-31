import sqlite3
from config import config

CREATE_TABLE_STRING = '''CREATE TABLE IF NOT EXISTS registrations
                    (client_uuid, server_uuid, created)'''

DROP_TABLE_STRING = "DROP TABLE IF EXISTS registrations"

INSERT_STRING = """INSERT INTO registrations
                VALUES (?, ?, ?)"""

SELECT_STRING = """SELECT * FROM registrations
                WHERE client_uuid = ?
                AND server_uuid = ?"""


class Database:
    connection = None
    cursor = None

    def __init__(self):
        self.connection = sqlite3.connect(
            config['database']['database_name']
        )
        self.cursor = self.connection.cursor()

    def create_table(self):
        self.cursor.execute(CREATE_TABLE_STRING)
        self.connection.commit()

    def drop_table(self):
        self.cursor.execute(DROP_TABLE_STRING)
        self.connection.commit()

    def insert_registration(self, client_uuid, server_uuid, date_create):
        self.cursor.execute(INSERT_STRING, (client_uuid, server_uuid, date_create))
        self.connection.commit()

    def select_one_registration(self, client_uuid, server_uuid):
        self.cursor.execute(SELECT_STRING, (client_uuid, server_uuid))
        return self.cursor.fetchone()

    def close_connection(self):
        self.connection.close()