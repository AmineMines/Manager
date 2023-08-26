import mysql.connector

class MySQLDatabase:

    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = None
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
            print("Disconect")

    def execute_query(self, query):
        try:
            cursor = self.connection.cursor()
            cursor.execute(query)
            self.connection.commit()
            print("Query successful excuted")
        except mysql.connector.Error as err:
            print("Error when excuting query", err)
        nvjvk