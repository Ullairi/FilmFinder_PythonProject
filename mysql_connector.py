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

# Find films by keyword function
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


# Find films by genre and release year range
def search_by_genre_year(category_id, min_year, max_year, limit=10, offset=0):
    genre_year_query = """
            SELECT f.film_id, f.title, f.release_year, f.description
            FROM film f
            JOIN film_category fc ON fc.film_id = f.film_id
            WHERE fc.category_id = %s
            AND f.release_year BETWEEN %s AND %s
            ORDER BY f.release_year, f.title
            LIMIT %s OFFSET %s;
    """

    with connect() as conn:
        cursor = conn.cursor()
        cursor.execute(genre_year_query, (category_id,min_year, max_year,limit,offset))
        return cursor.fetchall()