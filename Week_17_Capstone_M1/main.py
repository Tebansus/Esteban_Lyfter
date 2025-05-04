from menu_logic import menu_operation
from menu_gui import create_menu_window
from db_operations import create_database

# Main function to initialize the application.
# It creates the database if it doesn't exist and then opens the menu window.
# It also starts the event loop to process button clicks and other events.
def main():
    
    # Create the database if it doesn't exist
    create_database()
   
    window = create_menu_window()
    # Event loop to process button clicks and other events
    menu_operation(window)
    
if __name__ == "__main__":
    main()