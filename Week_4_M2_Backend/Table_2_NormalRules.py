import sqlite3
import os

if os.path.exists("Table2.db"):
    os.remove("Table2.db")

conn = sqlite3.connect("Table2.db")

cursor = conn.cursor()
# First we prepare the data for insertion and also create the Vehicles table.
vehicles_data = [
    ["VIN",        "Make",      "Model", "Year", "Color", "Owner ID",
     "Owner Name", "Owner Phone", "Insurance Company", "Insurance Policy"],

    ["1HGCM82633A", "Honda",     "Accord", 2003, "Silver",
     101, "Alice",  "123-456-7890", "ABC Insurance", "POL12345"],

    ["1HGCM82633A", "Honda",     "Accord", 2003, "Silver",
     102, "Bob",    "987-654-3210", "XYZ Insurance", "POL54321"],

    ["5J6RM4H79EL", "Honda",     "CR-V",   2014, "Blue",
     103, "Claire", "555-123-4567", "DEF Insurance", "POL67890"],

    ["1G1RA6EH1FU", "Chevrolet", "Volt",   2015, "Red",
     104, "Dave",   "111-222-3333", "GHI Insurance", "POL98765"]
]

cursor.execute('''
CREATE TABLE Vehicles (
    VIN VarChar(20) NOT NULL,
    Make VarChar(25) NOT NULL,
    Model VarChar(25) NOT NULL,
    Year INT NOT NULL,
    Color VarChar(15) NOT NULL,
    OwnerID INT NOT NULL,
    OwnerName VarChar(40) NOT NULL,
    OwnerPhone VarChar(15) NOT NULL,
    InsuranceCompany VarChar(40) NOT NULL,
    InsurancePolicy VarChar(15) NOT NULL
)
''')
conn.commit()
cursor.executemany('''INSERT INTO Vehicles (VIN, Make, Model, Year, Color, OwnerID, OwnerName, OwnerPhone, InsuranceCompany, InsurancePolicy) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?) ''', vehicles_data[1:])
conn.commit()

# Now, lets analyze the normal nature of the table.
# First, for 1NF, we need to ensure that all attributes are atomic.
# In this case, all attributes are atomic as there a reno complex entries, so the table is in 1NF.
# Then, for 2NF, we need to ensure that all non-key attributes are fully functionally dependent on the primary key.
# The primary key is composite (VIN, OwnerID), and some attributes are dependent on OwnerID only.
# And others on VIN only.
# So, we need to split the table into two tables: Vehicles and Owners.
# We also need to create two junction tables to maintain the relationships.
# First, a VechicleOwnerShip table to maintain the relationship between Vehicles and Owners.
# And then an insurance table to maintain the relationship between Owners and Insurance.

# Lets start by creating the Owners table.

cursor.execute('''
CREATE TABLE Owners (
    OwnerID INT NOT NULL PRIMARY KEY,
    OwnerName VarChar(40) NOT NULL,
    OwnerPhone VarChar(15) NOT NULL
)
''')
conn.commit()

cursor.execute('''
    SELECT DISTINCT OwnerID, OwnerName, OwnerPhone FROM Vehicles
''')
owners_data = cursor.fetchall()
# Insert data into the Owners table
cursor.executemany('''INSERT INTO Owners (OwnerID, OwnerName, OwnerPhone) VALUES (?, ?, ?) ''', owners_data)
conn.commit()

# Now, lets create the VehicleOwnership table, which will be the junction table between Vehicles and Owners.
cursor.execute('''
CREATE TABLE VehicleOwnership (
    VIN VarChar(20) NOT NULL REFERENCES Vehicles(VIN),
    OwnerID INT NOT NULL REFERENCES Owners(OwnerID)
)
''')
conn.commit()
# Extract the data from the Vehicles table and insert it into the VehicleOwnership table
cursor.execute('''
    SELECT VIN, OwnerID FROM Vehicles
''')
vehicle_ownership_data = cursor.fetchall()
# Insert data into the VehicleOwnership table
cursor.executemany('''INSERT INTO VehicleOwnership (VIN, OwnerID) VALUES (?, ?) ''', vehicle_ownership_data)
conn.commit()
# Finally, lets handle the insurance data.
# We will create a new table for Insurance and a junction table for Policy.
cursor.execute('''
CREATE TABLE Policy (
    PolicyNo VARCHAR(15) PRIMARY KEY,
    Company  VARCHAR(40) NOT NULL
)
''')
conn.commit()

# lets select the distinct insurance policies and companies from the Vehicles table.
cursor.execute('''
    SELECT DISTINCT InsurancePolicy, InsuranceCompany FROM Vehicles
''')

insurance_data = cursor.fetchall()
# Insert data into the Policy table
cursor.executemany('''INSERT INTO Policy (PolicyNo, Company) VALUES (?, ?) ''', insurance_data)
conn.commit()

# Now, lets create the PolicyOwnership table, which will be the junction table between Owners and Policy.
cursor.execute('''
CREATE TABLE OwnerPolicy (
    OwnerID  INT         NOT NULL REFERENCES Owners(OwnerID),
    PolicyNo VARCHAR(15) NOT NULL REFERENCES Policy(PolicyNo)
    
)
''')
conn.commit()

# Now, lets extract the data from the Vehicles table and insert it into the OwnerPolicy table.
cursor.execute('''
    SELECT DISTINCT OwnerID, InsurancePolicy FROM Vehicles
''')

owner_policy_data = cursor.fetchall()
# Insert data into the OwnerPolicy table
cursor.executemany('''INSERT INTO OwnerPolicy (OwnerID, PolicyNo) VALUES (?, ?) ''', owner_policy_data)
conn.commit()



# Now, lets drop the Vehicle table columns that are not needed in the Vehicles table.
cursor.execute('ALTER TABLE VEhicles DROP COLUMN OwnerID')
cursor.execute('ALTER TABLE Vehicles DROP COLUMN OwnerName')
cursor.execute('ALTER TABLE Vehicles DROP COLUMN OwnerPhone')
cursor.execute('ALTER TABLE Vehicles DROP COLUMN InsuranceCompany')
cursor.execute('ALTER TABLE Vehicles DROP COLUMN InsurancePolicy')

conn.commit()

cursor.execute('''
DELETE FROM Vehicles
WHERE rowid NOT IN (
    SELECT MIN(rowid)
    FROM   Vehicles
    GROUP  BY VIN, Make, Model, Year, Color
);

        ''')
conn.commit()
# Withh all of the above, we have achieved 2NF.
#Finally, to comply with the 3NF rule, we need to remove transitive dependencies.
# The only transitive dependency is for make and model.
# So, we will create a new table called models to separate the make and model.

cursor.execute('''
CREATE TABLE Models (
    
    Model VarChar(25) NOT NULL,
    Make VarChar(25) NOT NULL
)            
'''
)
conn.commit()
# Now, lets extract the data from the Vehicles table and insert it into the Models table.
cursor.execute('''
    SELECT DISTINCT Model, Make FROM Vehicles
''')
Makes_data = cursor.fetchall()
# Insert data into the Models table
cursor.executemany('''INSERT INTO Models (Model, Make) VALUES (?, ?) ''', Makes_data)
conn.commit()
#Now, lets remove the Make from the Vehicles table.
cursor.execute('ALTER TABLE Vehicles DROP COLUMN Make')

conn.commit()
cursor.close()
conn.close()