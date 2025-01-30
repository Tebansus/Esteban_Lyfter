#!/usr/bin/env python
# coding: utf-8

# In[1]:


def main():
    # File containing song names, one per line
    input_file = "songs.txt"  
    # File to save sorted song names
    output_file = "sorted_songs.txt"  
    try:
        # Open the input file to read song names
        with open(input_file, "r", encoding="utf-8") as file:
            song_names = file.readlines()

        # Remove white space and sort the names
        song_names = [song.strip() for song in song_names]
        song_names.sort()

        # Write the sorted names to the ouput file
        with open(output_file, "w", encoding="utf-8") as file:
            for song in song_names:
                file.write(song + "\n")       
    # Except to catch file not found or file opening error. 
    except FileNotFoundError:
        print(f"Error: The file '{input_file}' was not found.")
    except IOError as e:
        print(f"An I/O error occurred: {e}")

if __name__ == "__main__":
    main()

