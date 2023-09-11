import random
import string

import mysql.connector


class MySQLDatabase:

    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.connection = None
        self.database = database
        self.connect()

    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database

            )
            print("Successfull connection")
        except mysql.connector.Error as err:
            print("Error when connection", err)

    def disconnect(self):
        if self.connection:
            self.connection.close()


    def execute_query(self, query):
        try:
            cursor = self.connection.cursor()
            cursor.execute(query)

            if cursor.description is not None:

                result = cursor.fetchall()
                return result
            else:

                self.connection.commit()
                return None

        except mysql.connector.Error as err:
            print("Error when executing query", err)
            return None

    def insert_data(self, passwords):
            try:
                cursor = self.connection.cursor()
                for website, credentials in passwords.items():
                    username = credentials['username']
                    password = credentials['password']

                    query = f"INSERT INTO passwords (website, username, password) VALUES ('{website}', '{username}', '{password}')"
                    cursor.execute(query)
                    self.connection.commit()



                print("inserted successfully.")
            except mysql.connector.Error as err:
                print("Error when inserting data", err)
