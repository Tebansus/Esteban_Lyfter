from menu import display_menu
from menu import menu_functionality
def main():
    # Initialize an empty dictionary to store student data
    students_base = {}
    
    # Start an infinite loop to display the menu and process user input
    while True:
        # Display the menu options
        display_menu()  
        
        try:
            # Get user input and convert it to an integer
            choice = int(input("Enter your choice: "))
            
            # Check if the choice is between 1 and 7
            if 1 <= choice <= 7:
                # Call the menu_functionality function with the user's choice and the student data
                result = menu_functionality(choice, students_base)
                
                # Update the student data with the result from menu_functionality
                students_base = result
                
                # If the user clicks 7, print a thank you message and break the loop
                if result == "Ending":
                    print("Thank you for using our service.")
                    break
            else:
                # If the choice is not between 1 and 7, prompt the user to enter a valid choice
                print("Please enter a valid choice between 1 and 7.")
        except ValueError:
            # If the input is not a valid integer, prompt the user to enter a valid choice
            print("Please enter a valid choice.")     

if __name__ == "__main__":
    main() 
