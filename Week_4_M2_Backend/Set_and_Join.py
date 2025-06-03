##########################################################################
##########################Set Exercises###################################
##########################################################################
'''


All = {1,2,3,4,5,6,7,8,9,10}
Even = {2,4,6,8,10}
Odd = {1,3,5,7,9}


Even U Odd = {2,4,6,8,10,1,3,5,7,9}

Even ∩ Odd= {}

All - odd = {2,4,6,8,10}

C(even) = {1,3,5,7,9}

C(odd-all) = {2,4,6,8,10}



'''


##########################################################################
#######################Join SQL Exercises#################################
##########################################################################
import sqlite3
import os

if os.path.exists("Library.db"):
    os.remove("Library.db")
conn = sqlite3.connect("Library.db")
cursor = conn.cursor()


#Book data (Name, AuthorID)
Books_Data = [
    ["Don Quijote",1],
    ["La Divina Comedia",2],
    ["Vagabond 1-3",3],
    ["Dragon Ball 1",4],
    ["The Book of the 5 Rings", None]
]

#Author data (Name)
Authors_Data = [
    ["Miguel de Cervantes"],
    ["Dante Alighieri"],
    ["Takehiko Inoue"],
    ["Akira Toriyama"],
    ["Walt Disney"]
]

#customer data (Name, Email)
Customers_Data = [
    ["John Doe",  "j.doe@email.com"],
    ["Jane Doe",  "jane@doe.com"],
    ["Luke Skywalker", "darth.son@email.com"]
]

# Rent data (BookID, CustomerID, State)
Rents_Data = [
    [1, 2, "Returned"],
    [2, 2, "Returned"],
    [1, 1, "On time"],
    [3, 1, "On time"],
    [2, 2, "Overdue"]
    
]

# Execute to create the tables. Define all the table and the respective columns and relationships.
cursor.executescript('''
    CREATE TABLE Books (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    Name VARCHAR(50) NOT NULL,
    AuthorID INTEGER REFERENCES Authors(ID)
);

    CREATE TABLE Authors (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    Name VARCHAR(50) NOT NULL
);
    CREATE TABLE Customers (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    Name VARCHAR(50) NOT NULL,
    Email VARCHAR(50) NOT NULL
);

    CREATE TABLE Rents (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    BookID INTEGER REFERENCES Books(ID),
    CustomerID INTEGER REFERENCES Customers(ID),
    State VARCHAR(20) NOT NULL
);



''')

conn.commit()

# Now, we insert the data into the tables.

cursor.executemany(''' INSERT INTO Books (Name, AuthorID) VALUES (?, ?)''', Books_Data)
cursor.executemany(''' INSERT INTO Authors (Name) VALUES (?)''', Authors_Data)
cursor.executemany(''' INSERT INTO Customers (Name, Email) VALUES (?, ?)''', Customers_Data)
cursor.executemany(''' INSERT INTO Rents (BookID, CustomerID, State) VALUES (?, ?, ?)''', Rents_Data)
conn.commit()
# Now, we proceed with the select queries assigned in this exercise. First, we begin by printing all the books and their respective authors, including those without authors.
cursor.execute('''
               SELECT b.Name, a.Name
               FROM Books as b
               LEFT JOIN Authors as a 
               ON b.AuthorID = a.ID
            
               
               
               ''')

# Save the results in a variable and print them.
Book_author_pairs = cursor.fetchall()
print("Books and their Authors")
for book, author in Book_author_pairs:
    print(f"{book} by {author}")
    
# Next, we will select book names that have no authors associated with them.
cursor.execute('''
               SELECT  DISTINCT b.Name
               FROM Books as b
               LEFT JOIN Authors as a 
               ON b.AuthorID = a.ID
               WHERE b.AuthorID IS NULL;
               
               
               ''')
# Then, we print the books that have no authors.
books_no_author = cursor.fetchall()
print("\nBooks with no Author:")
for book,  in books_no_author:
    print(f"{book} Has no author")
# For the third query, we will select authors that have no books associated with them.  
cursor.execute('''
               SELECT DISTINCT a.Name
               FROM Books as b
               RIGHT JOIN Authors as a 
               ON b.AuthorID = a.ID
               WHERE b.AuthorID IS NULL;
               
               
               ''')
# Save them in a variable and print them.
authors_no_books = cursor.fetchall()
print("\nAuthors with no Books:")
for author, in authors_no_books:
    print(f"{author} has no books")

# Forth query, we will select the book names that have been rented before only.
cursor.execute('''
               SELECT DISTINCT b.Name
               FROM Books as b
               INNER JOIN Rents as a 
               ON b.ID = a.BOOKID
              
               
               
               ''')
# Then, we save the results in a variable and print them.
rented_books = cursor.fetchall()
print("\nBooks that have been rented:")
for book, in rented_books:
    print(f"{book} has been rented")
# Fifth query, we will select the book names that have never been rented.
cursor.execute('''
               SELECT DISTINCT b.Name
               FROM Books as b
               LEFT JOIN Rents as a 
               ON b.ID = a.BOOKID
               WHERE a.BookID IS NULL;
               
               
               ''')
# Save the results in a variable and print them.
books_not_rented = cursor.fetchall()
print("\nBooks that have never been rented:")
for book, in books_not_rented:
    print(f"{book} has never been rented")
# Sixth query, we will select the customers that have never rented a book.
cursor.execute('''
               SELECT DISTINCT b.Name
               FROM Customers as b
               LEFT JOIN Rents as a 
               ON b.ID = a.CustomerID
               WHERE a.CustomerID IS NULL;
               
               
               ''')
# Save the results in a variable and print them.
customers_havent_rented = cursor.fetchall()
print("\nCustomers that have never rented a book:")
for customer, in customers_havent_rented:
    print(f"{customer} has never rented a book")
# Seventh query, we will select the books that have been rented and also fall under the category of overdue books. 
cursor.execute('''
                SELECT DISTINCT b.Name
                FROM Books AS b
                INNER JOIN Rents AS a 
                    ON b.ID = a.BOOKID
                WHERE a.State = 'Overdue'
            ''')
overdue_books = cursor.fetchall()
print("\nOverdue Books:")
for book, in overdue_books:
    print(f"{book} is overdue")