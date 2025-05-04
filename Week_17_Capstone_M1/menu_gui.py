import FreeSimpleGUI as sg

# This function creates the main menu window for the Money Management System.
# It includes buttons for resetting the tool, adding a category, withdrawing money, adding money, and exiting the application.
# It also includes a table to display movements with columns for date, title, category, amount, and resulting balance.

def create_menu_window():
    # Left column with buttons
    left_column = [
        [sg.Button("Reset Tool", size=(15, 2), pad=(10, 10))],
        [sg.Button("Add Category", size=(15, 2), pad=(10, 10))],
        [sg.Button("Withdraw", size=(15, 2), pad=(10, 10))],
        [sg.Button("Add_Money", size=(15, 2), pad=(10, 10))],
        [sg.Button("Exit", size=(15, 2), pad=(10, 10))]
    ]
    right_column = [
        [sg.Text("Movements", justification='left', size=(20, 1)),
         sg.Push()],
        [sg.Table(
            values=[["" for _ in range(5)] for _ in range(10)],
            headings=["date", "Title", "Category", "amount", "resulting_balance"],
            auto_size_columns=True,
            justification='center',
            num_rows=10,
            key='-TABLE-',
            expand_x=True,
            expand_y=True
        )]
    ]
    layout = [
        [sg.Text("Money Management System", font=("Helvetica", 12), justification='center', expand_x=True)],
        [sg.Column(left_column, vertical_alignment='top'), 
         sg.Column(right_column, expand_x=True, expand_y=True)]
    ]
    
    # Create the window, the finalize=True argument is used to finalize the window layout
    # before displaying it, allowing for dynamic elements to be added later if needed.
    window = sg.Window(title = "Menu", layout = layout, margins = (100, 100), finalize=True)
    
    

    return window