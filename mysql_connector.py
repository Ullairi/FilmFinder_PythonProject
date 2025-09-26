import os
import dotenv
from pathlib import Path
import pymysql

dotenv.load_dotenv(Path('.env'))

# Connection to database
dbconfig = {'host': os.environ.get('host'),
            'user': os.environ.get('user'),
            'password': os.environ.get('password'),
            'database': os.environ.get('db_sql')}

# Create and return connection to MySql
def connect():
    return pymysql.connect(**dbconfig)

# Find film by keyword function
def search_by_keyword(keyword, limit=10,offset=0):
    search_query = """
                SELECT film_id, title
                FROM film
                WHERE title LIKE %s
                ORDER BY title
                LIMIT %s OFFSET %s;
    """

    with connect() as conn:
        cursor = conn.cursor()
        cursor.execute(search_query, (f"%{keyword}%",limit,offset))
        return cursor.fetchall()