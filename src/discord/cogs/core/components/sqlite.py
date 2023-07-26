import sqlite3
from sqlite3 import Error

class DBManager:

    def __init__(self, db_file):
        """ initialize database connection and cursor """
        self.conn = None
        self.cursor = None
        self.db_file = db_file
        
        self.startup()


    def startup(self):
        with open("src/discord/cogs/core/components/sql/create_tables.sql", 'r') as f:
            sql_commands = f.read().split(';')

        for command in sql_commands:
            if command.strip():
                self.execute_query(command)

    def connect(self):
        """ create a database connection to the SQLite database """
        try:
            self.conn = sqlite3.connect(self.db_file)
            self.cursor = self.conn.cursor()
        except Error as e:
            print(e)

    def execute_query(self, query, params=()):
        """ execute a single query """
        if self.conn is None or self.cursor is None:
            self.connect()

        try:
            self.cursor.execute(query, params)
            self.conn.commit()
        except Error as e:
            print(e)

    def fetch_results(self, query, params=()):
        """ execute a query and fetch results """
        if self.conn is None or self.cursor is None:
            self.connect()

        try:
            self.cursor.execute(query, params)
            rows = self.cursor.fetchall()
            return rows
        except Error as e:
            print(e)

    def close(self):
        """ close the connection """
        if self.cursor is not None:
            self.cursor.close()
        if self.conn is not None:
            self.conn.close()
