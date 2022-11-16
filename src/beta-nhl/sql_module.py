import mysql.connector
from mysql.connector import Error
import pandas as pd

# Function below is reuseable!
def create_server_connection(host_name, user_name, user_password):
  ''' Creates a connection to local MySQL server '''
  connection = None
  try:
    connection = mysql.connector.connect(
      host=host_name,
      user=user_name,
      passwd=user_password
    )
    print("MySQL Database connection successful")
  except Error as err:
    print(f"Error: '{err}'")

  return connection

# Function below is reusable!
def create_db_connection(host_name, user_name, user_password, db_name):
  ''' Creates a connection to a specified database on local MySQL server '''
  connection = None
  try:
    connection = mysql.connector.connect(
      host=host_name,
      user=user_name,
      passwd=user_password,
      database=db_name
    )
    print("MySQL Database connection successful")
  except Error as err:
    print(f"Error: '{err}'")

  return connection

# Function below is reusable!
def create_database(connection, query):
  cursor = connection.cursor()
  try:
    cursor.execute(query)
    print("Database created successfully")
  except Error as err:
    print(f"Error: '{err}'")

# Function below is reusable!
def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Query successful")
    except Error as err:
        print(f"Error: '{err}'")