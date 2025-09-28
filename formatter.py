from mysql_connector import SQLConnector

class Formatter:
    def __init__(self):
        self.db = SQLConnector()

#   Function to search films by a keyword entered by user
#   Prints  film ID, title, and description
    def search_films_keyword(self):
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

            # Show list of films and print formatted info
            for film in films:
                film_id, title, description = film
                print(f"# {film_id} | {title}\nDescription:\n{description}\n" + "-" * 70)

            if len(films) < limit:
                break

            # Ask user if he wants to see 10 next results
            count = input("Show next 10 films? (y/n): ").lower()
            if count != "y":
                break
            offset += limit


    # Function that shows available genres
    def  search_films_by_genre_and_year(self):
        print("\n<-- Available Genres -->")
        genres = self.db.genre_list()
        for g in genres:
            print(f"{g[0]}: {g[1]}")

    #   Shows available year range
        year = self.db.year_range()
        print(f"\n<-- Available year range: {year[0]} - {year[1]} -->")

        try: # Ask user for genre id and year range
            category_id = int(input("Enter genre category ID: "))
            min_year = int(input("Enter start year: "))
            max_year = int(input("Enter end year: "))
        except ValueError: # If user will type non-numeric input
            print("Invalid input. Please enter only numbers")
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

            if len(films) < limit:
                break

            # Ask user if he wants to see 10 next results
            count = input("Show next 10 films? (y/n): ").lower()
            if count != "y":
                break
            offset += limit