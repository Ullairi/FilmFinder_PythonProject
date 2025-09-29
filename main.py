from log_stats import LogStats
from formatter import Formatter

fr = Formatter() # Created Formatter instance to handle search and display
stats = LogStats() # Created LogStats instance to handle statistics search

# Main Menu function for Film Finder
# Display options for the user to choose from and return their choice

def main_menu():
    print("\n< ------------ FIlM FINDER ------------ 2>")
    print("1. Search films by keyword")
    print("2. Search films by genre and year range")
    print("3. Show top 5 search results")
    print("4. Show last 5 search results")
    print("5. Exit")
    choice = input("Enter your choice: ")
    return choice.strip()

# Entry point of the program
if __name__ == "__main__":
    while True:
        choice = main_menu()

        if choice == "1":
            fr.search_films_keyword() # Search film using keyword
        elif choice == "2":
            fr.search_films_by_genre_and_year() # Search film by genre and year range
        elif choice == "3":
            top = stats.top_queries(5) # Shows top 5 search queries
            print("\nTop 5 search results:")
            stats.queries_output(top)
        elif choice == "4":
           last = stats.last_queries(5) # Shows last 5 search queries
           print("\nLast 5 search results:")
           stats.queries_output(last)
        elif choice == "5":
            print("Thank you for using this program. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.") # In case of invalid input