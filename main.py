import os
import dotenv
from pathlib import Path
import pymysql
from formatter import search_films_keyword, search_films_by_genre_and_year


# Main Menu function for Film Finder
# Display options for the user to choose from and return their choice

def main_menu():
    print("\n< ------------ FIlM FINDER ------------ 2>")
    print("1. Search films by keyword")
    print("2. Search films by genre and year range")
    print("3. Exit")
    choice = input("Enter your choice: ")
    return choice.strip()


if __name__ == "__main__":
    while True:
        choice = main_menu()

        if choice == "1":
            search_films_keyword()
        elif choice == "2":
            search_films_by_genre_and_year()
        elif choice == "3":
            print("Thank you for using this program. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")