
import FreeSimpleGUI as sg
from db_operations import reset_db
from db_operations import add_category_db
from db_operations import get_categories
from db_operations import add_money_to_db
from db_operations import load_data
from db_operations import withdraw_money_from_db
from datetime import datetime, timezone
from clases import Category
from clases import Transaction
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
# Validation is handled by the decorators in the Category class.
def add_category():
    category_name = sg.popup_get_text("Enter the category name:")
    try:
        # Create a Category object - validation happens in the decorators
        category_obj = Category(category_name)
        
        # If validation passes, add to database
        if add_category_db(category_obj.name):            
            sg.popup(f"Category '{category_obj.name}' added successfully!")
        else:
            sg.popup(f"Category '{category_obj.name}' already exists.")
            
    except ValueError as errore:
        sg.popup(str(errore))
# This function creates a popup window to add money to a specific category in the database.
# If the category does not exist, it prompts the user to enter a valid category.
# It also includes an input field for the type of income.
# Validation is handled by the decorators in the Transaction class.
def add_money():   
    
    categories_for_popup = get_categories()
    
    layout = [
        [sg.Text("Enter the category:")],
        [sg.Combo(values=categories_for_popup, key='-CATEGORY-', readonly=True)],
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
            try:
                # Get current UTC time
                current_utc_time = datetime.now(timezone.utc)    
                amount = values['amount']
                category = values['-CATEGORY-']
                type_income = values['Type_of_Income']               
               
                transaction = Transaction(current_utc_time, amount, type_income, category)               
                add_money_to_db(transaction)
                sg.popup(f"Added {transaction.amount} in category '{transaction.category}'")
                break
                
            except ValueError as e:
                sg.popup(str(e))
    
    window_popup.close()
# This function creates a popup window to withdraw money from a specific category in the database.
# It includes an input field for the type of withdrawal.
# If the category does not exist, it prompts the user to enter a valid category.
# It also checks if the withdrawal amount exceeds the available balance in the account.
def withdraw_func():   
    
    categories_for_popup_withdraw = get_categories()
    layout = [
        [sg.Text("Enter the category:")],
        [sg.Combo(values=categories_for_popup_withdraw, key='-CATEGORY-', readonly=True)],
        [sg.Text("Enter the amount to withdraw:")],        
        [sg.InputText(key='amount')],
        [sg.Text("Enter the type of withdrawal:")],
        [sg.InputText(key='Type_of_Wthdrawl')],
        [sg.Button("Withdraw"), sg.Button("Cancel")]
    ]
    window_popup_withdraw = sg.Window("Withdraw Money", layout)
    
    while True:
        event, values = window_popup_withdraw.read()
        if event == sg.WIN_CLOSED or event == "Cancel":
            break
        if event == "Withdraw":
            try:
                # Get current UTC time
                current_utc_time = datetime.now(timezone.utc)           
               
                amount = values['amount']
                category = values['-CATEGORY-']
                type_withdrawl = values['Type_of_Wthdrawl']        
                
                transaction = Transaction(current_utc_time, amount, type_withdrawl, category)
                
                # If validation passes, attempt withdrawal from database
                if withdraw_money_from_db(transaction):
                    sg.popup(f"Withdrew {transaction.amount} from category '{transaction.category}'")
                    break
                else:
                    sg.popup(f"You can't withdraw more money than exists in the account. Please add more or revise your withdrawal amount.")
                    
            except ValueError as e:
                # Show validation error message in a popup
                sg.popup(str(e))
                
    window_popup_withdraw.close()

