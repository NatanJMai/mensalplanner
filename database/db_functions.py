import mysql.connector
import configparser
from mysql.connector import Error
import pandas as pd

def connect_on_database():
    connection = None
    config  = reading_from_file()
    user    = config['mysql']['user']
    host    = config['mysql']['host']
    passwd  = config['mysql']['passwd']
    query   = None

    connection = create_server_connection(host, user, passwd)
    execute_query(connection, "USE mensalplanner;")
    return connection

def start_database():
    connection = connect_on_database()

    # TRY TO CONNECT ON DATABASE MENSALPLANNER,
    # If YES, we already have the database.
    # If NOT, we don't have created yet.
    query = "USE mensalplanner;"

    if not execute_query(connection, query):
        query = "CREATE DATABASE mensalplanner;"
        execute_query(connection, query)
        execute_query(connection, "USE mensalplanner;")

    print(("The database has been created!"))
    create_tables(connection)
    return

# Reading database config file (db.ini).
def reading_from_file():
    config = configparser.ConfigParser()
    config.read('db.ini')

    config['mysql']['host']
    config['mysql']['user']
    config['mysql']['passwd']
    config['mysql']['db']
    return config

# Execute query received as parameter
def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        #print("Query successful!")
    except Error as err:
        print(f"Error '{err}'")
        return False
    return True

# Create server connection with host, user and password.
def create_server_connection(host_name, user_name, user_password):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            password=user_password)
        #print("Database has been connected!")
    except Error as err:
        print(f"Error: '{err}'")
    return connection

# Create all tables
def create_tables(connection):
    # Creating tables (TASK, LABEL and USER)

    create_user_table = """
    CREATE TABLE user 
    (user_id            INT PRIMARY KEY AUTO_INCREMENT,
     user_name          VARCHAR(255) NOT NULL,
     user_password      VARCHAR(255) NOT NULL);
     """

    create_label_table = """
    CREATE TABLE label
        (label_id           INT PRIMARY KEY AUTO_INCREMENT,
         label_name         VARCHAR(255) NOT NULL,
         label_description  VARCHAR(255) NOT NULL, 
         label_color        VARCHAR(255) NOT NULL);
        """

    create_task_table = """
    CREATE TABLE task 
    (task_id            INT PRIMARY KEY AUTO_INCREMENT,
     task_name          VARCHAR(255)  NOT NULL,
     task_description   VARCHAR(255) NOT NULL,
     task_datetime      DATE NOT NULL,
     user            INT NOT NULL,
     label           INT,
     FOREIGN KEY (user) REFERENCES user(user_id),
     FOREIGN KEY (label) REFERENCES label(label_id));
     """

    execute_query(connection, create_user_table)
    execute_query(connection, create_label_table)
    execute_query(connection, create_task_table)
    return

# Function to read a query from database connection.
def read_query(connection, query):
    result = None
    cursor = connection.cursor()

    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as err:
        print(f"Error: '{err}'")


