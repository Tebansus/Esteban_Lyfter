import PySimpleGUI as sg
from operatrions import reset_tool
from operatrions import add_category
from operatrions import add_money
from operatrions import reset_table
from operatrions import withdraw_func

# This function creates the main menu window for the Money Management System.
# It responds to the clicks of the buttons and performs the corresponding operations.
# It calls the reset_tool function to reset the tool, the add_category function to add a new category,
# the add_money function to add money to a category, and the withdraw_func function to withdraw money.
# It also resets the table to reflect the latest data after each operation.
def menu_operation(window): 
    reset_table(window)
    while True:        
        event, values = window.read()       
        if event == sg.WIN_CLOSED or event == "Exit":
            break
        if event == "Reset Tool":            
            reset_tool()
            reset_table(window)           
        if event == "Add Category":
            add_category()
        if event == "Add_Money":
            add_money()
            reset_table(window)
        if event == "Withdraw":
            withdraw_func()
            reset_table(window)

    window.close()
    