
import os
import csv
from datetime import datetime, timezone
## Reset the database to its initial state
# This function will delete the existing csv files and create new ones with the same headers
# It also resets the balance to 0 in the total_tracker table
def reset_db():
    with open("users.csv", "w", newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["date", "Title", "Category", "amount", "resulting_balance"])
    with open("categories.csv", "w", newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["category_name"])
    with open("total_tracker.csv", "w", newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Total_Balance"])
        writer.writerow([0])
   
   
# Connect to SQLite database or create it if it doesn't exist.
# Create the necessary tables if they don't exist.
# If the table is empty, insert the default value of 0 into the total_tracker table, else do nothing.
def create_database():
    if not os.path.exists("users.csv"):
        with open("users.csv", "w", newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["date", "Title", "Category", "amount", "resulting_balance"])
    if not os.path.exists("categories.csv"):
        with open("categories.csv", "w", newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["category_name"])
    if not os.path.exists("total_tracker.csv"):
        with open("total_tracker.csv", "w", newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Total_Balance"])
            writer.writerow([0])
    else:
        with open("total_tracker.csv", "r") as file:
            reader = csv.reader(file)
            rows = list(reader)
            if len(rows) <= 1:
                with open("total_tracker.csv", "a", newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow([0])
# This function will add a new category to the categories table
# It checks if the category already exists before adding it
# If the category already exists, it returns False, otherwise it returns True
def add_category_db(category_name):
    # Check if the category already exists
    categories = get_categories()
    if category_name in categories:
        return False
    else:
        # Append the new category to categories.csv
        with open('categories.csv', 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([category_name])
        return True
    
# This function will load the data from the users table and return it as a list of tuples.
# It will be used to populate the table in the GUI.
def load_data():    
    if not os.path.exists('users.csv'):
        return []
    
    with open('users.csv', 'r', newline='') as f:
        reader = csv.reader(f)
        next(reader) 
        data = []
        for row in reader:            
            if len(row) >= 5:                
                try:
                    row[3] = float(row[3])
                    row[4] = float(row[4])
                except ValueError:
                    
                    row[3] = 0
                    row[4] = 0
                data.append(tuple(row))
    return data
# This function will retrieve all categories from the categories table and return them as a list
# It will be used to populate the dropdown menu for adding money or withdrawing money.
def get_categories():
    if not os.path.exists('categories.csv'):
        return []
    
    with open('categories.csv', 'r', newline='') as file:
        reader = csv.reader(file)
        next(reader) 
        return [row[0] for row in reader if row] 
# This function will add money to the database
# It will insert a new record into the users table with the current date, title, category, amount, and resulting balance
# It will also update the total balance in the total_tracker table
def add_money_to_db(transaction_object):     
       
    # Get the current total balance
    total_to_modify = 0.0
    if os.path.exists('total_tracker.csv'):
        with open('total_tracker.csv', 'r', newline='') as f:
            reader = csv.reader(f)
            next(reader, None)  
            try:
                row = next(reader, None)
                if row:
                    total_to_modify = float(row[0])
            except (StopIteration, ValueError):
                total_to_modify = 0
      
    # Append the transaction to users.csv
    with open('users.csv', 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([
            transaction_object.date,
            transaction_object.type_transaction,
            transaction_object.category,
            transaction_object.amount,
            total_to_modify + transaction_object.amount
        ])
    # Update the total balance in total_tracker.csv
    with open('total_tracker.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Total_Balance'])
        writer.writerow([total_to_modify + transaction_object.amount])
        
        
        
# This function will withdraw money from the database
# It will insert a new record into the users table with the current date, title, category, amount, and resulting balance
def withdraw_money_from_db(transaction_object):     
    
    # Get the current total balance
    total_to_modify = 0
    if os.path.exists('total_tracker.csv'):
        with open('total_tracker.csv', 'r', newline='') as f:
            reader = csv.reader(f)
            next(reader, None)  #
            try:
                row = next(reader, None)
                if row:
                    total_to_modify = float(row[0])
            except (StopIteration, ValueError):
                total_to_modify = 0
    
    # Check if the balance is sufficient
    if total_to_modify - transaction_object.amount >= 0:        
        # Append the transaction to users.csv
        with open('users.csv', 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([
                transaction_object.date,
                transaction_object.type_transaction,
                transaction_object.category,
                -transaction_object.amount,  # Negative amount for withdrawals
                total_to_modify - transaction_object.amount
            ])        
        # Update the total balance in total_tracker.csv
        with open('total_tracker.csv', 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Total_Balance'])
            writer.writerow([total_to_modify - transaction_object.amount])
        
        return True
    else:
        return False
    
    