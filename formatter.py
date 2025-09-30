from mysql_connector import SQLConnector
from log_writer import LogWriter

class Formatter:
    def __init__(self):
        self.db = SQLConnector() # MySQL connector for film query
        self.log = LogWriter() # MongoDB logger for statistics searches


    def show_more(self,limit,offset):
        """
        Ask user if they want see next page of results
        Returns updated offset if user confirm, in other case None
        """
        count=input("Show next 10 films? (y/n): ").lower()
        if count == "y":
            return offset + limit
        else:
            return None

    def log_search(self, search_type: str, params: dict, results, more_info: str = ""):
        """ Function to log search results to database with optional info """
        self.log.search_log(
            search_type=search_type,
            params=params,
            films_found=len(results),
            more_info=more_info
        )


    def search_films_keyword(self):
        """ Function to search films by keywords """
        keyword = input("Enter keyword to find film titles: ")
        offset = 0
        limit = 10
        header = False

        while True:
            films = self.db.search_by_keyword(keyword, limit, offset)
            if not films:
                print("No films were found") # Message to user in case search returns nothing
                break

            if not header:
                print("\n< ID | Title >") # Header title for first row
                header = True

            # Show list of films
            for film in films:
                film_id, title, description = film
                print(f"# {film_id} | {title}\nDescription:\n{description}\n" + "-" * 70)

            self.log_search("keyword", {"keyword": keyword}, films, more_info=f"{keyword}")

            if len(films) < limit:
                break

            # Check if user need to see next page
            sh_more = self.show_more(limit, offset)
            if sh_more is None:
                break
            offset = sh_more


    def  search_films_by_genre_and_year(self):
        """ Function to search films by genre and year """
        print("\n<-- Available Genres -->")
        genres = self.db.genre_list()
        for genr in genres:
            print(f"{genr[0]}: {genr[1]}")

        # Shows available year range
        year = self.db.year_range()
        print(f"\n<-- Available year range: {year[0]} - {year[1]} -->")


        try: # Ask user for genre id
            category_id = int(input("Enter genre category ID: "))
        except ValueError: # If user will type non-numeric input
            print("Invalid input. Please enter only numbers")
            return

        # Category_id check
        categ_id = [genre[0] for genre in genres]
        if category_id not in categ_id:
            print(f"Invalid category ID. Please choose category from {categ_id}.")
            return


        try: # Ask user to enter the year range
            min_year = int(input("Enter start year: "))
            max_year = int(input("Enter end year: "))
        except ValueError:
            print("Invalid input. Please enter only numbers")
            return

        # Year range check
        minimal_year, maximal_year = year[0], year[1]
        if min_year < minimal_year or max_year > maximal_year or min_year > max_year:
            print(f"Invalid input. Please enter years within the {minimal_year} - {maximal_year} range")
            return

        offset = 0
        limit = 10
        header = False

        while True:
            films = self.db.search_by_genre_year(category_id, min_year, max_year, limit, offset)
            if not films:
                print("No films were found")
                break

            if not header:
                print("\n< ID | Title | Year >")
                header = True

            for film in films: # Shows list of films and print formatted info
                film_id, title, release_date, description = film
                print(f"# {film_id} | {title} | {release_date}\nDescription:\n{description}\n" + "-" * 70)

            # Get genre name for logging
            genre_name = next((genr[1] for genr in genres if genr[0] == category_id), str(category_id))

            self.log.search_log(
                search_type="genre",
                params={"category_id": category_id, "min_year": min_year, "max_year": max_year},
                films_found=len(films),
                more_info=f"{genre_name} | Year range: {min_year} - {max_year}"
            )

            if len(films) < limit:
                break

            # Ask user if he wants to see 10 next results
            sh_more = self.show_more(limit, offset)
            if sh_more is None:
                break
            offset = sh_more