import mysql.connector
from config.environment import MYSQL_HOST, MYSQL_PORT, MYSQL_USERNAME, MYSQL_PASSWORD, MYSQL_DATABASE

class Database:
    def __init__(self):
        self.host = MYSQL_HOST
        self.port = MYSQL_PORT
        self.user = MYSQL_USERNAME
        self.password = MYSQL_PASSWORD
        self.database = MYSQL_DATABASE
    
    def get_connection(self):
        return mysql.connector.connect(
            host=self.host,
            port=self.port,
            user=self.user,
            password=self.password,
            database=self.database,
            ssl_ca="cert.pem",
            ssl_verify_cert=True,
            ssl_verify_identity=True
        )
    
    def close_connection(self, connection):
        if connection.is_connected():
            connection.close()
        else:
            print("Connection is already closed.")