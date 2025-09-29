import os
import dotenv
from pathlib import Path
import pymysql

dotenv.load_dotenv(Path('.env'))

class SQLConnector:
    """ Class created to handle connection and queries to MySQL database"""
    def __init__(self):
        self.dbconfig = {'host': os.environ.get('HOST'),
            'user': os.environ.get('USER'),
            'password': os.environ.get('PASSWORD'),
            'database': os.environ.get('DB_SQL')
        }

    def connect(self):
        """ Connects to MySQL database"""
        return pymysql.connect(**self.dbconfig)

    def cursor_execute(self, query, params=None, fetch_one=False):
        """ Executes query and returns results"""
        with self.connect() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, params)
                return cursor.fetchone() if fetch_one else cursor.fetchall()

    def search_by_keyword(self, keyword, limit=10,offset=0):
        """Returns films when searching by keyword"""
        search_query = """
                SELECT film_id, title,description
                FROM film
                WHERE title LIKE %s
                ORDER BY title
                LIMIT %s OFFSET %s;
        """
        return self.cursor_execute(search_query,(f"%{keyword}%", limit, offset))


    def genre_list(self):
        """ Show list of all genres"""
        genre_query = """
                SELECT category_id, name
                FROM category
                ORDER BY name;
        """
        return self.cursor_execute(genre_query)


    def year_range(self):
        """Returns minimum and maximum release year range"""
        year_query = """
                SELECT MIN(release_year) AS min_year, MAX(release_year) AS max_year
                FROM film;
        """
        return self.cursor_execute(year_query, fetch_one=True)


    def search_by_genre_year(self, category_id, min_year, max_year, limit=10, offset=0):
        """Returns films when searching by genre or release year"""
        genre_year_query = """
                SELECT f.film_id, f.title, f.release_year, f.description
                FROM film f
                JOIN film_category fc ON fc.film_id = f.film_id
                WHERE fc.category_id = %s
                AND f.release_year BETWEEN %s AND %s
                ORDER BY f.release_year, f.title
                LIMIT %s OFFSET %s;
        """

        return self.cursor_execute(genre_year_query, (category_id,min_year, max_year,limit,offset))