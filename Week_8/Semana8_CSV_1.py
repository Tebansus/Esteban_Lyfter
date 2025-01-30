#!/usr/bin/env python
# coding: utf-8

# In[1]:


import csv
# Function to receive each game, which is called for however many games the suer wants to input. It then saves it to a dictionary and returns it.
def get_game_info():
    try:
        name = input("Enter the game's name: ")
        genre = input("Enter the game's genre: ")
        developer = input("Enter the developer: ")
        rating = input("Enter the  rating (E, T, M): ")
        return { "name": name, "genre": genre, "developer": developer, "classification": rating,}
    except Exception as e:
        print(f"An error ocurred for the information: {e}")
        return None
# After it finishes asking the user, save it in a csv with the dict writter function based on the defined keys.
def save_to_csv(file_name, games):
    try:
        with open(file_name, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=["name", "genre", "developer", "classification"])
            writer.writeheader()
            writer.writerows(games)       
    except Exception as e:
        print(f"An error occurred while the games to the csv: {e}")
# Main function to call the logging functions. 
def main():
    try:
        num_games = int(input("How many games would you like to enter? "))
        games = []

        for i in range(num_games):
            game_info = get_game_info()
            if game_info:
                games.append(game_info)
        if games:
            save_to_csv("Saved_Games_List.txt", games)
            print("Games Saved, program done.")
        else:
            print("No game data exists, please enter some data.")
    except ValueError:
        print("Invalid input. Please enter a valid number of games to enter into the system.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()

