import csv
import psycopg2

# Create a class to manage the creation of tables and population of data
class TableCreatorRepo:
    def __init__(self, db_manager):
        self.db_manager = db_manager
    # Start the creation of tables with the necessary SQL queries
    def create_tables(self):
        queries = [
            """
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                email VARCHAR(50) UNIQUE NOT NULL,
                username VARCHAR(50) UNIQUE NOT NULL,
                password VARCHAR(50) NOT NULL,
                date_of_birth DATE NOT NULL,
                state_of_account VARCHAR(20) DEFAULT 'ACTIVE'
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS cars(
                id SERIAL PRIMARY KEY,
                make VARCHAR(50) NOT NULL,
                model VARCHAR(50) NOT NULL,
                year INT NOT NULL,
                rented_state VARCHAR(20) DEFAULT 'AVAILABLE'
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS car_renters (
                id SERIAL PRIMARY KEY,
                user_id INT NOT NULL,
                car_id INT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
                FOREIGN KEY (car_id) REFERENCES cars(id) ON DELETE CASCADE, 
                date_rented TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                rent_status VARCHAR(20) DEFAULT 'ONGOING'
            );
            """               
           
       
        ]
        # Execute each query to create the tables and also create an index for rented cars to ensure that no car can be rented twice at the same time.
        for query in queries:
            self.db_manager.execute_query(query)
        index_query = """
                CREATE UNIQUE INDEX IF NOT EXISTS uniq_rented_car
                ON car_renters(car_id)
                WHERE rent_status = 'ONGOING';
         """
        self.db_manager.execute_query(index_query)
    # Table population methods to read mock data from CSV files and insert it into the respective tables.
    def populate_table_users(self):
        with open('mock_data.csv', 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                query = """
                    INSERT INTO users (name, email, username, password, date_of_birth, state_of_account)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    ON CONFLICT (email) DO NOTHING;
                """
                params = (row['name'], row['email'], row['username'], row['password'], row['date_of_birth'], row['state_of_account'])
                self.db_manager.execute_query(query, params)
    # This method populates the cars table with mock data from a CSV file, but only if the table is empty to ensure it isnt loaded twice.
    def populate_table_cars_first_pass(self):
        # Check if the table is empty
        check_query = "SELECT 1 FROM cars LIMIT 1"
        result = self.db_manager.execute_query(check_query)
        table_is_empty = not result

        if table_is_empty:
            with open('mock_car_data.csv', 'r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    insert_query = """
                        INSERT INTO cars (make, model, year)
                        VALUES (%s, %s, %s)
                    """
                    params = (row['make'], row['model'], row['year'])
                    self.db_manager.execute_query(insert_query, params)
    # This method populates the car_renters table with mock data from a CSV file, but only if the table is empty to ensure it isnt loaded twice.
    def populate_table_car_renters(self):
        #Check if the table is empty
        check_query = "SELECT 1 FROM car_renters LIMIT 1"
        result = self.db_manager.execute_query(check_query)
        table_is_empty = not result
        if table_is_empty:
            with open('mock_data_user_rentals.csv', 'r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    query = """
                        INSERT INTO car_renters (user_id, car_id, date_rented, rent_status)
                        VALUES (%s, %s, %s, %s)
                    """
                    params = (row['user_id'], row['car_id'], row['date_rented'], row['rent_status'])
                    try:
                        self.db_manager.execute_query(query, params)
                    except psycopg2.errors.UniqueViolation as e:
                        print(f"Duplicate RENTED car for car_id={row['car_id']} - skipping entry.")
                        # Optionally, log to a file or list
                        self.db_manager.connection.rollback()  # IMPORTANT: reset after error
                    except Exception as e:
                        print(f"Other error: {e}")
                        self.db_manager.connection.rollback()  # Always rollback after errors
    # This method adjusts the rented state of cars based on the current rentals in the car_renters table, only used for initial setup.
    def adjust_car_rented_state(self):
        query = """
            UPDATE cars
            SET rented_state = 'RENTED'
            WHERE id IN (
                SELECT car_id FROM car_renters WHERE rent_status = 'ONGOING'
            );
        """
        self.db_manager.execute_query(query)
        
        