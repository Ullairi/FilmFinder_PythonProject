from mysql_connector import (search_by_keyword, genre_list, year_range, search_by_genre_year)

# Function to search films by a keyword entered by user
# Prints  film ID, title, and description

def search_films_keyword():
    keyword = input("Enter keyword to find film titles: ")
    offset = 0
    limit = 10
    header = False

    while True:
        films = search_by_keyword(keyword, limit, offset)
        if not films:
            print("No films were found") # Message to user in case search returns nothing
            break

        if not header:
            print("\n<ID | Title>") # Header title for first row
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