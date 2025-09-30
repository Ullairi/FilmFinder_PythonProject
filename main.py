from log_stats import LogStats
from formatter import Formatter

fr = Formatter() # Created Formatter instance to handle search and display
stats = LogStats() # Created LogStats instance to handle statistics search

# Main Menu function for Film Finder
# Display options for the user to choose from and return their choice

def main_menu():
    print("\n< ------------ FIlM FINDER ------------ >")
    print("1. Search films by keyword")
    print("2. Search films by genre and year range")
    print("3. Statistics")
    print("4. Exit")
    choice = input("Enter your choice: ")
    return choice.strip()

def log_menu():
    print("\n< ------------ Statistics ------------ >")
    print("1. Top 5 searches")
    print("2. Last 5 searches")
    print("3. Return to main menu")
    choice = input("Enter your choice: ").strip()
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
            while True:
                log_choice = log_menu()
                if log_choice == "1":
                    top = stats.top_queries(5) # Shows top 5 search queries
                    print("\nTop 5 search results:")
                    stats.queries_output(top)
                    input("\nPress enter to continue...")
                elif log_choice == "2":
                    last = stats.last_queries(5)
                    print("\nLast 5 search results:")
                    stats.queries_output(last)
                    input("\nPress enter to return to statistics menu...")
                elif log_choice == "3":
                    break
                else:
                    print("\nInvalid choice. Try again")
        elif choice == "4":
            print("Thank you for using this program. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.") # In case of invalid input