import sqlite3
import os

if os.path.exists("Table1.db"):
    os.remove("Table1.db")

# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect("Table1.db")
cursor = conn.cursor()

orders_data = [
    ('001', 'Alice',  '123-456-7890', '123 Main St',    101, 'Cheeseburger',  8.00, 2, 'No onions',     '6:00 PM'),
    ('001', 'Alice',  '123-456-7890', '123 Main St',    102, 'Fries',         3.00, 1, 'Extra ketchup', '6:00 PM'),
    ('002', 'Bob',    '987-654-3210', '456 Elm St',     103, 'Pizza',        12.00, 1, 'Extra cheese',  '7:30 PM'),
    ('002', 'Bob',    '987-654-3210', '456 Elm St',     104, 'Fries',         2.00, 2, None,            '7:30 PM'),
    ('003', 'Claire', '555-123-4567', '789 Oak St',     105, 'Salad',         6.00, 1, 'No croutons',   '12:00 PM'),
    ('004', 'Claire', '555-123-4567', '464 Georgia St', 106, 'Water',         1.00, 1, None,            '5:00 PM')
]

cursor.execute('''
CREATE TABLE Orders (
    OrderID INT NOT NULL,
    CustomerName VarChar(50) NOT NULL,
    CustomerPhone VarChar(15) NOT NULL,
    CustomerAddress VarChar(100) NOT NULL,
    ItemID INT NOT NULL,
    ItemName VarChar(50) NOT NULL,
    ItemPrice DECIMAL(20, 2) NOT NULL,
    ItemQuantity INT NOT NULL,
    SpecialRequest VarChar(100),
    OrderTime VarChar(10) NOT NULL
)
''')
conn.commit()
# Insert data into the Orders table
cursor.executemany('''INSERT INTO Orders (OrderID, CustomerName, CustomerPhone, CustomerAddress, ItemID, ItemName, ItemPrice, ItemQuantity, SpecialRequest, OrderTime) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?) ''', orders_data)

conn.commit()

# Now, lets start by fixing the data with the 2NF rule. The 1NF rule is already satisfied as we have a primary composite key (OrderID, ItemID) and no repeating groups. 
# So now the 2NF rule is to remove partial dependencies.
# We will create a new table for items  and another for order-items, which will be the junction table between orders and items.

cursor.execute('''
CREATE TABLE Items (
    ItemID INT NOT NULL PRIMARY KEY,
    ItemName VarChar(50) NOT NULL,
    ItemPrice DECIMAL(20, 2) NOT NULL
);


'''
)
conn.commit()
cursor.execute('''
    SELECT DISTINCT ItemID, ItemName, ItemPrice FROM Orders
    
''')
items_data = cursor.fetchall()
# Insert data into the Items table
cursor.executemany('''INSERT INTO Items (ItemID, ItemName, ItemPrice) VALUES (?, ?, ?) ''', items_data)
conn.commit()


# Now, lets create the OrderItems table, which will be the junction table between Orders and Items.
cursor.execute('''
CREATE TABLE OrderItems (
    OrderID INT NOT NULL REFERENCES Orders(OrderID),
    ItemID INT NOT NULL REFERENCES Items(ItemID),
    ItemQuantity INT NOT NULL,
    SpecialRequest VarChar(100)
)
''')
conn.commit()

# Extract the data from the Orders table and insert it into the OrderItems table
cursor.execute('''
    SELECT DISTINCT OrderID, ItemID, ItemQuantity, SpecialRequest FROM Orders

''')

Order_items_data = cursor.fetchall()
# Insert data into the OrderItems table
cursor.executemany('''INSERT INTO OrderItems (OrderID, ItemID, ItemQuantity, SpecialRequest) VALUES (?, ?, ?, ?) ''', Order_items_data)
conn.commit()


# Delete the ItemID, ItemName and ItemPrice from the Orders table
cursor.execute('ALTER TABLE Orders DROP COLUMN ItemID')
cursor.execute('ALTER TABLE Orders DROP COLUMN ItemName')
cursor.execute('ALTER TABLE Orders DROP COLUMN ItemPrice')
cursor.execute('ALTER TABLE Orders DROP COLUMN ItemQuantity')
cursor.execute('ALTER TABLE Orders DROP COLUMN SpecialRequest')
conn.commit()

# Now, after all oh this, we have the schema compliant with the 2NF rule.
# Now, we must start to make changes to comply with the 3NF rule.
# The 3NF rule is to remove transitive dependencies.
# In this case we have the CustomerName, CustomerPhone and CustomerAddress as transitive dependencies, so we move them to a new table called Customers.

cursor.execute('''
CREATE TABLE Customers (
    CustomerID INTEGER PRIMARY KEY AUTOINCREMENT,
    CustomerName VarChar(50) NOT NULL,
    CustomerPhone VarChar(15) NOT NULL,
    CustomerAddress VarChar(100) NOT NULL
)
''')
conn.commit()
# Now we will insert the data into the Customers table.
cursor.execute('''
    SELECT DISTINCT CustomerName, CustomerPhone, CustomerAddress FROM Orders
''')
customers_data = cursor.fetchall()
# Insert data into the Customers table
cursor.executemany('''INSERT INTO Customers (CustomerName, CustomerPhone, CustomerAddress) VALUES (?, ?, ?) ''', customers_data)
conn.commit()
# Now we will add the CustomerID to the Orders table
cursor.execute('ALTER TABLE Orders ADD COLUMN CustomerID INTEGER REFERENCES Customers(CustomerID)')
# Now, we will populate the CustomerID in the Orders table
cursor.execute('''
    UPDATE Orders
    SET CustomerID = (
        SELECT CustomerID
        FROM Customers
        WHERE Customers.CustomerName = Orders.CustomerName
        AND Customers.CustomerPhone = Orders.CustomerPhone
        AND Customers.CustomerAddress = Orders.CustomerAddress
    )
''')
conn.commit()
cursor.execute('''
DELETE FROM Orders
WHERE rowid NOT IN (
    SELECT MIN(rowid)
    FROM   Orders
    GROUP  BY OrderID, OrderTime, CustomerID, CustomerName, CustomerPhone
);

        ''')
conn.commit()
# Now we will delete the CustomerName, CustomerPhone and CustomerAddress from the Orders table
cursor.execute('ALTER TABLE Orders DROP COLUMN CustomerName')
cursor.execute('ALTER TABLE Orders DROP COLUMN CustomerPhone')
cursor.execute('ALTER TABLE Orders DROP COLUMN CustomerAddress')

cursor.close()
conn.close()


