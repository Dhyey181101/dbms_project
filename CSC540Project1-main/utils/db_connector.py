import mysql.connector
from mysql.connector import Error
import configparser

class DatabaseConnectionManager:
    _connection = None  # Static variable for shared connection

    def __init__(self):
        pass

    def get_connection():
        if not DatabaseConnectionManager._connection:
            DatabaseConnectionManager._connection, cursor = DatabaseConnectionManager.establishConnection()
        return DatabaseConnectionManager._connection

    def establishConnection():
        config = configparser.ConfigParser()
        config.read('db_config.ini')
        mysql_config = config['mysql']

        connection = mysql.connector.connect(
            host=mysql_config['host'],
            user=mysql_config['user'],
            password=mysql_config['password'],
            database=mysql_config['database'],
        )

        if connection.is_connected():
            print("Connection Established")
            cursor = connection.cursor()
            print("Cursor Created")
        
        return connection, cursor
        
    def close_connection():
        if DatabaseConnectionManager._connection:
            cursor = DatabaseConnectionManager.create_cursor(DatabaseConnectionManager._connection)
            if cursor:
                cursor.close()
            DatabaseConnectionManager._connection.close()
            print("Connection closed.")
            DatabaseConnectionManager._connection = None  # Reset static variable

    def create_cursor(connection):
        cursor = None
        if connection.is_connected():
            cursor = connection.cursor()
        return cursor

    def check_if_connected():
        if DatabaseConnectionManager._connection:
            return DatabaseConnectionManager._connection.is_connected()
        return False


if __name__ == "__main__":
    db_manager = DatabaseConnectionManager()    
    connection = db_manager.get_connection()
    
    db_manager.close_connection()
