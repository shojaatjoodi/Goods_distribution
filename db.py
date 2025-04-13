# This module handles the connection to the MySQL database for the distribution system.
# It includes functions to connect to the database, close the connection, and handle errors.
# 
# import mysql.connector

# def connect_db(): # Establish a connection to the MySQL database 
#     try:
#         connection = mysql.connector.connect(
#             host="localhost",
#             user="shoja89",  # Replace with your MySQL username
#             password="Shj504#@8921",  # Replace with your MySQL password
#             database="distribution_system"
#         )
#         if connection.is_connected():
#             print("Connected to the database successfully!")
#         return connection
    
#     except mysql.connector.Error as err:
#         print(f"Error: {err}")
#         return None

# def close_database_connection(connection):
#     if connection and connection.is_connected():
#         connection.close()
#         print("Database connection closed.")

# This module handles the connection to the MySQL database for the distribution system.
# It includes functions to connect to the database, close the connection, and handle errors.
# 
import mysql.connector
import os
import logging
from mysql.connector import Error

# from dotenv import load_dotenv  
# # Load environment variables from .env file
# load_dotenv()

from dotenv import load_dotenv
# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def connect_db():
    """Establish a connection to the MySQL database."""
    try:
        connection = mysql.connector.connect(
            host=os.getenv("DB_HOST", "localhost"),
            user=os.getenv("DB_USER"),  # Fetch from environment variables
            password=os.getenv("DB_PASSWORD"),  # Fetch from environment variables
            database=os.getenv("DB_NAME", "distribution_system"),
            auth_plugin='mysql_native_password'  # Use native password authentication for MySQL
        )
        if connection.is_connected():
            logging.info("Connected to the database successfully!")
        return connection
    
    except Error as err:
        logging.error(f"Database connection error: {err}")
        return None

def close_database_connection(connection):
    """Close the database connection."""
    if connection and connection.is_connected():
        connection.close()
        logging.info("Database connection closed.")