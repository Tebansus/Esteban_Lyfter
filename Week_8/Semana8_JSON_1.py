#!/usr/bin/env python
# coding: utf-8

# In[1]:


import json

def read_pokemon_data(file_path):
    # Open the file if it exists. If it doesn't, create a new file instead in the root folder.
    try:
        with open(file_path, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"File '{file_path}' not found. A new one will be created instead in the root.")
        return []
    except json.JSONDecodeError:
        print(f"File '{file_path}' is not a JSON file, creating a new one in the root folder.")
        return []

def save_pokemon_data(file_path, data):
   # Open the file and use the dump function to add new pokemon.
    with open(file_path, "w") as file:
        json.dump(data, file, indent=2)
        print("New Pokemon Added.")
   

def get_pokemon_info():
    try:
        # Take the names and types. 
        name = input("Enter Pokémon name: ").strip()
        types = input("Enter Pokémon types (comma-separated): ").strip().split(",")
        types = [t.strip() for t in types]
        # Create base stat dictionary to append to the JSON
        poke_stats = {}
        for stat in ["HP", "Attack", "Defense", "Sp. Attack", "Sp. Defense", "Speed"]:
            poke_stats[stat] = int(input(f"Enter Pokémon {stat}: "))

        return {
            "name": {
                "english": name
            },
            "type": types,
            "base": poke_stats
        }
    except ValueError as e:
        print("Invalid stat. Please input numeric whole values for the stats.")
        return None

def main():
    file_path = "pokemon_data.json"
    # Read existing Pokémon data if available
    pokemon_data = read_pokemon_data(file_path)

    # Get the new Pokemon information. 
    new_pokemon = get_pokemon_info()
    # If the inputs are invalid, dont add it to the json and exit.
    if new_pokemon is None:
        print("Couldn't add new pokemon because the inputs aren't valid.")
        return

    # Add new Pokémon to the data
    pokemon_data.append(new_pokemon)

    # Save updated Pokémon data to the file.
    save_pokemon_data(file_path, pokemon_data)

if __name__ == "__main__":
    main()

