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


# Get list of all available genres
def genre_list():
    genre_query = """
    SELECT category_id, name
    FROM category
    ORDER BY name;
    """

    with connect() as conn:
        cursor = conn.cursor()
        cursor.execute(genre_query)
        return cursor.fetchall()


# Get min. and max. release year range from films
def year_range():
    year_query = """
    SELECT MIN(release_year) AS min_year, MAX(release_year) AS max_year
    FROM film;
    """

    with connect() as conn:
        cursor = conn.cursor()
        cursor.execute(year_query)
        return cursor.fetchone()