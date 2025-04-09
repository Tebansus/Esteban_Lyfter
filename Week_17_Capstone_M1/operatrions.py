
import FreeSimpleGUI as sg
from db_operations import reset_db
from db_operations import add_category_db
from db_operations import get_categories
from db_operations import add_money_to_db
from db_operations import load_data
from db_operations import withdraw_money_from_db

# This function calls the reset_db function to reset the database and confirm with the user before proceeding.
def reset_tool():
    confirm = sg.popup_yes_no("Are you sure you want to reset the tool?")
    if confirm == "Yes":
        sg.popup("Tool reset successfully!")
        reset_db()
# This function updates the table in the GUI with the latest data from the database.
def reset_table(window):
    data_to_load = load_data()
    window["-TABLE-"].update(data_to_load)
# This function creates a popup window to add a new category to the database.
def add_category():
    category = sg.popup_get_text("Enter the category name:")
    if category:
        if add_category_db(category):            
            sg.popup(f"Category '{category}' added successfully!")
        else:
            sg.popup(f"Category '{category}' already exists.")
    else:
        sg.popup("No category entered.")
# This function creates a popup window to add money to a specific category in the database.
# If the category does not exist, it prompts the user to enter a valid category.
# It also includes an input field for the type of income.
def add_money():
    categories_for_popup = get_categories()
    
    layout = [
        [sg.Text("Enter the category:")],
        [sg.Combo(values=categories_for_popup, key='-CATEGORY-')],
        [sg.Text("Enter the amount to add:")],        
        [sg.InputText(key='amount')],
        [sg.Text("Enter the type of income:")],
        [sg.InputText(key='Type_of_Income')],
        [sg.Button("Add"), sg.Button("Cancel")]
    ]
    window_popup = sg.Window("Add Money", layout)
    
    while True:
        event, values = window_popup.read()
        if event == sg.WIN_CLOSED or event == "Cancel":
            break
        if event == "Add":
            amount = values['amount']
            category = values['-CATEGORY-']
            type_income = values['Type_of_Income']
            try:
                amount = float(amount)
                if amount <= 0:
                    sg.popup("Please enter a positive amount.")
                    continue
                elif category:                    
                    add_money_to_db(amount, category, type_income)
                    sg.popup(f"Added {amount} in category '{category}'")
                else:                    
                    sg.popup("Please enter a category first.")
            except ValueError:
                sg.popup("Invalid amount entered. Please enter a number.")
        break
    window_popup.close()
# This function creates a popup window to withdraw money from a specific category in the database.
# It includes an input field for the type of withdrawal.
# If the category does not exist, it prompts the user to enter a valid category.
# It also checks if the withdrawal amount exceeds the available balance in the account.
def withdraw_func():
    categories_for_popup_withdraw = get_categories()
    layout = [
        [sg.Text("Enter the category:")],
        [sg.Combo(values=categories_for_popup_withdraw, key='-CATEGORY-')],
        [sg.Text("Enter the amount to withdraw:")],        
        [sg.InputText(key='amount')],
        [sg.Text("Enter the type of withdrawl:")],
        [sg.InputText(key='Type_of_Wthdrawl')],
        [sg.Button("Withdraw"), sg.Button("Cancel")]
    ]
    window_popup_withdraw = sg.Window("Withdraw Money", layout)
    
    while True:
        event, values = window_popup_withdraw.read()
        if event == sg.WIN_CLOSED or event == "Cancel":
            break
        if event == "Withdraw":
            amount = values['amount']
            category = values['-CATEGORY-']
            type_withdrawl = values['Type_of_Wthdrawl']
            try:
                amount = float(amount)
                if amount <= 0:
                    sg.popup("Please enter a positive amount.")
                    continue
                elif category:
                    if withdraw_money_from_db(amount, category, type_withdrawl):
                        sg.popup(f"Withdrew {amount} in category '{category}'")
                    else:
                        sg.popup(f"You can't withdraw more money than there exists in the account. Please add more or revise your withdrawl amount.")
                else:                    
                    sg.popup("Please enter a category first.")
            except ValueError:
                sg.popup("Invalid amount entered. Please enter a number.")
        break
    window_popup_withdraw.close()

