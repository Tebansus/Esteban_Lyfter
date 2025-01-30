#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# Define menu function to avoid Rework
def display_menu(current_number):
        print("\nCurrent number:", current_number)
        print("Choose an operation:")
        print("1. Add")
        print("2. Subtract")
        print("3. Multiply")
        print("4. Divide")
        print("5. Clear result")
        print("6. Exit")


def main():
    # ALways start current number at 0.
    current_number = 0  
    # Start the menu and loop to be used constantly until user decides to stop.
    while True:
        try:
            # Main try Except which catches unexpected errors.
            display_menu(current_number)
            choice = input("Enter your choice (1-6): ").strip()
            # Read the choice. if it isn't 1-6, ask the user for another input. If it is 6, end. If it is 5, clear number.
            if choice == '6':
                print("Exiting the calculator.")
                break
    
            if choice not in {'1', '2', '3', '4', '5'}:
                print("Invalid option. Please select a number between 1 and 6.")
                continue

            if choice == '5':
                current_number = 0
                print("Result cleared. Current number reset to 0.")
                continue
            # If the choice is 1-4, ask for another number for the operation. 
            new_number = input("Enter a number: ").strip()
            # Try to convert this number to float with try except. If value error, ask the user for another input.
            try:
                new_number = float(new_number)
            except ValueError:
                print("Invalid input. Please enter a valid number, float or int.")
                continue
            # Execute the operations for each choice, check if inout number is 0 for division to avoid undefined errors.
            if choice == '1':
                current_number += new_number
            elif choice == '2':
                current_number -= new_number
            elif choice == '3':
                current_number *= new_number
            elif choice == '4':
                if new_number == 0:
                    print("Error: Division by zero is not permitted.")
                    continue
                current_number /= new_number

        except Exception as e:
            print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()

