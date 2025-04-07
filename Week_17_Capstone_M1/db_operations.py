import sqlite3
from datetime import datetime, timezone
## Reset the database to its initial state
# This function will drop the existing tables and create new ones
# It also resets the balance to 0 in the total_tracker table
def reset_db():
    # Connect to SQLite database
    conn = sqlite3.connect('expense_database.db')
    cursor = conn.cursor()

    # Drop the  tables if they exist
    cursor.execute("DROP TABLE IF EXISTS users")
    cursor.execute("DROP TABLE IF EXISTS categories")
    cursor.execute("DROP TABLE IF EXISTS total_tracker")

    # Create a new set of tables
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        date TEXT,
        Title TEXT,
        Category TEXT,
        amount REAL,
        resulting_balance REAL
    )
    '''
    )
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS categories (
        category_name TEXT PRIMARY KEY       
    )
    '''
    )
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS total_tracker (
        Total_Balance REAL       
    )
    '''
    )
    cursor.execute('INSERT INTO total_tracker (Total_Balance) VALUES (0)')
    
    # Commit and close the connection
    conn.commit()
    conn.close()
# Connect to SQLite database or create it if it doesn't exist.
# Create the necessary tables if they don't exist.
# If the table is empty, insert the default value of 0 into the total_tracker table, else do nothing.
def create_database():
    
    conn = sqlite3.connect('expense_database.db')
    cursor = conn.cursor()

    # Create a table for user data
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        date TEXT,
        Title TEXT,
        Category TEXT,
        amount REAL,
        resulting_balance REAL
    )
    '''
    )
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS categories (
        category_name TEXT PRIMARY KEY       
    )
    '''
    )
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS total_tracker (
        Total_Balance REAL       
    )
    '''
    )
    # Check if the table is empty
    cursor.execute('SELECT COUNT(*) FROM total_tracker')
    row_count = cursor.fetchone()[0]

    
    if row_count == 0:
        cursor.execute('INSERT INTO total_tracker (Total_Balance) VALUES (0)')
    
    
    conn.commit()
    conn.close()

# This function will add a new category to the categories table
# It checks if the category already exists before adding it
# If the category already exists, it returns False, otherwise it returns True
def add_category_db(category_name):
    conn = sqlite3.connect('expense_database.db')
    cursor = conn.cursor()
    # Check if the category already exists
    cursor.execute("SELECT * FROM categories WHERE category_name = ?", (category_name,))
    existing_category = cursor.fetchone()
    if existing_category:
        conn.close()
        return False
    else:
        # Insert the new category into the categories table
        cursor.execute("INSERT INTO categories (category_name) VALUES (?)", (category_name,))
        conn.commit()
        conn.close()
        return True
    
# This function will load the data from the users table and return it as a list of tuples.
# It will be used to populate the table in the GUI.
def load_data():    
    conn = sqlite3.connect('expense_database.db')
    cursor = conn.cursor()   
    cursor.execute("SELECT * FROM users")
    data = cursor.fetchall()   
    conn.close()
    return data
# This function will retrieve all categories from the categories table and return them as a list
# It will be used to populate the dropdown menu for adding money or withdrawing money.
def get_categories():
    conn = sqlite3.connect('expense_database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT category_name FROM categories")
    categories = [row[0] for row in cursor.fetchall()]
    conn.close()
    return categories
# This function will add money to the database
# It will insert a new record into the users table with the current date, title, category, amount, and resulting balance
# It will also update the total balance in the total_tracker table
def add_money_to_db(amount_add, category, type_income):     
    
    current_utc_time = datetime.now(timezone.utc)
    conn = sqlite3.connect('expense_database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT Total_Balance FROM total_tracker")
    total_to_modify = cursor.fetchone()[0]
    
    cursor.execute("""INSERT INTO users
                   (date,
                   Title,
                   Category,
                   amount,
                   resulting_balance)
                   VALUES (?,?,?,?,?)                   
                   """
                   ,
                   (
                       current_utc_time,
                       type_income,
                       category,
                       amount_add,
                       total_to_modify + amount_add
                    
                   )
                   )
    cursor.execute("UPDATE total_tracker SET Total_Balance = ? WHERE rowid=1", (total_to_modify + amount_add,))
    conn.commit()
    conn.close()
# This function will withdraw money from the database
# It will insert a new record into the users table with the current date, title, category, amount, and resulting balance
def withdraw_money_from_db(amount_withdraw, category, type_income):     
    
    current_utc_time = datetime.now(timezone.utc)
    conn = sqlite3.connect('expense_database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT Total_Balance FROM total_tracker")
    total_to_modify = cursor.fetchone()[0]
    if total_to_modify - amount_withdraw >= 0:    
        cursor.execute("""INSERT INTO users
                    (date,
                    Title,
                    Category,
                    amount,
                    resulting_balance)
                    VALUES (?,?,?,?,?)                   
                    """
                    ,
                    (
                        current_utc_time,
                        type_income,
                        category,
                        -amount_withdraw,
                        total_to_modify - amount_withdraw
                        
                    )
                    )
        cursor.execute("UPDATE total_tracker SET Total_Balance = ? WHERE rowid=1", (total_to_modify - amount_withdraw,))
        conn.commit()
        conn.close()
        return True
    else:
        conn.commit()
        conn.close()
        return False
    
    