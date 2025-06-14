import psycopg2
from psycopg2 import sql
# This is the meat and potatoes of the code, the class that handles all the modifications to the database.
# It allows you to add users, add cars, modify account states, modify car rented states, generate new rentals, end rentals, disable cars, and retrieve all users, cars, and rentals.


class ModificationRepo:
    def __init__(self, db_manager):
        self.db_manager = db_manager
    # This is a helper method that builds a filtered query based on the base SQL, allowed columns, and filters.
    def build_filtered_query(self, base_sql, allowed_columns, filters):
        # If no filters are provided, return the base SQL without any WHERE clause.
        if not filters:
            return base_sql, ()
        #Else, build the WHERE clause based on the filters provided.
        conditions = []
        params = []
        for column, value in filters.items():
            if column not in allowed_columns:
                raise ValueError(f"Invalid filter column: {column}")
            # Append the condition to the list of conditions and the value to the list of parameters.
            conditions.append(sql.SQL("{} = %s").format(sql.Identifier(column)))
            params.append(value)
        # If there are conditions, append them to the base SQL.
        if conditions:
            base_sql = sql.SQL("{} WHERE ").format(sql.SQL(base_sql)) + sql.SQL(" AND ").join(conditions)
        return base_sql, tuple(params)
    # This method adds a new user to the database, checking for required fields and handling conflicts with existing emails.
    def add_user(self, name, email, username, password):
        if not all([name, email, username, password]):
            print("All fields are required.")
            return False
        
        query = """
            INSERT INTO users (name, email, username, password)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (email) DO NOTHING
            RETURNING id;
        """
        params = (name, email, username, password)
        result = self.db_manager.execute_query(query, params)
        if result and len(result) > 0:
            print("User added successfully!")
            return True
        else:
            print("Email already exists. User could not be added.")
            return False
    # This function adds a new car to the database, checking for required fields.
    def add_car(self, make, model, year):
        if not all([make, model, year]):
            print("All fields are required.")
            return False
        
        query = """
            INSERT INTO cars (make, model, year)
            VALUES (%s, %s, %s)
            RETURNING id;
        """
        params = (make, model, year)
        result = self.db_manager.execute_query(query, params)
        if result and len(result) > 0:
            print("Car added successfully!")
            return True
        else:
            print("Car could not be added.")
            return False
    # This method modifies the state of a user's account, checking for required fields and valid states.
    def modify_account_state(self, email, new_state):
        if not email or not new_state:
            print("Email and new state are required.")
            return False
        
        # Check if user exists
        check_query = "SELECT email FROM users WHERE email = %s;"
        result = self.db_manager.execute_query(check_query, (email,))
        if not result or len(result) == 0:
            print(f"User with email {email} does not exist.")
            return False

        if new_state not in ['ACTIVE', 'INACTIVE', 'DELETED', 'DEFAULTER']:
            print("Invalid state. Must be: ACTIVE, INACTIVE, DELETED or DEFAULTER.")
            return False
            
        query = """
            UPDATE users
            SET state_of_account = %s
            WHERE email = %s;
        """
        params = (new_state, email)
        self.db_manager.execute_query(query, params)
        print(f"Account state for {email} updated to {new_state}.")
        return True
    # This method modifies the rented state of a car, checking for required fields and valid states.
    def modify_car_rented_state(self, car_id, rented_state):
        if not car_id or not rented_state:
            print("Car ID and new rented_state are required.")
            return False

        # Check if car exists
        check_query = "SELECT id FROM cars WHERE id = %s;"
        result = self.db_manager.execute_query(check_query, (car_id,))
        if not result or len(result) == 0:
            print(f"Car with ID {car_id} does not exist.")
            return False

        if rented_state not in ['AVAILABLE', 'RENTED', 'UNAVAILABLE']:
            print("Invalid rent state. Must be: AVAILABLE, RENTED, UNAVAILABLE.")
            return False
            
        query = """
            UPDATE cars
            SET rented_state = %s
            WHERE id = %s;
        """
        params = (rented_state, car_id)
        self.db_manager.execute_query(query, params)
        print(f"rented_state for car ID {car_id} updated to {rented_state}.")
        return True
    # This method generates a new rental, checking for required fields, user existence, car existence, and car availability.
    def generate_new_rental(self, user_id, car_id):
        if not user_id or not car_id:
            print("User ID and Car ID are required.")
            return False

        # Check if user exists
        check_user_query = "SELECT id FROM users WHERE id = %s;"
        user_result = self.db_manager.execute_query(check_user_query, (user_id,))
        if not user_result or len(user_result) == 0:
            print(f"User with ID {user_id} does not exist.")
            return False

        # Check if car exists and fetch its rent_state
        check_car_query = "SELECT id, rented_state FROM cars WHERE id = %s;"
        car_result = self.db_manager.execute_query(check_car_query, (car_id,))
        if not car_result or len(car_result) == 0:
            print(f"Car with ID {car_id} does not exist.")
            return False

        # car_result will look like [(id, rent_state)]
        _, rent_state = car_result[0]
        if rent_state.lower() == 'unavailable':
            print(f"Car with ID {car_id} is currently unavailable for rent.")
            return False

        query = """
            INSERT INTO car_renters (user_id, car_id)
            VALUES (%s, %s)
            RETURNING id;
        """
        params = (user_id, car_id)
        try:
            result = self.db_manager.execute_query(query, params)
            if result and len(result) > 0:
                print("Rental created successfully!")
                return True
            else:
                print("Rental could not be created.")
                return False
        except psycopg2.errors.UniqueViolation:
            print("This car is already rented and has an ongoing rental.")
            return False
        
    # This method ends a rental, checking for required fields and rental existence, and updates the car condition to AVAILABLE.
    def end_rental(self, rental_id):
        if not rental_id:
            print("Rental ID is required.")
            return False
        
        # Check if rental exists
        check_query = "SELECT id FROM car_renters WHERE id = %s;"
        result = self.db_manager.execute_query(check_query, (rental_id,))
        if not result or len(result) == 0:
            print(f"Rental with ID {rental_id} does not exist.")
            return False

        query = """
            UPDATE car_renters
            SET rent_status = 'FINISHED'
            WHERE id = %s;
        """
        params = (rental_id,)
        self.db_manager.execute_query(query, params)
        print(f"Rental ID {rental_id} ended successfully.")
        
        # Update car condition to AVAILABLE
        update_car_query = """
            UPDATE cars
            SET rented_state = 'AVAILABLE'
            WHERE id = (SELECT car_id FROM car_renters WHERE id = %s);
        """
        self.db_manager.execute_query(update_car_query, (rental_id,))
        print(f"Car condition updated to AVAILABLE for rental ID {rental_id}.")
        
        return True
    # This method disables a car, checking for required fields and car existence.
    def disable_car(self, car_id):
        if not car_id:
            print("Car ID is required.")
            return False
        
        # Check if car exists
        check_query = "SELECT id FROM cars WHERE id = %s;"
        result = self.db_manager.execute_query(check_query, (car_id,))
        if not result or len(result) == 0:
            print(f"Car with ID {car_id} does not exist.")
            return False

        query = """
            UPDATE cars
            SET rented_state = 'UNAVAILABLE'
            WHERE id = %s;
        """
        params = (car_id,)
        self.db_manager.execute_query(query, params)
        print(f"Car ID {car_id} disabled successfully.")
        return True
    # This method retrieves all rented and available cars.
    def get_rented_and_available_cars(self):
        query = """
            SELECT id, make, model, year, rented_state
            FROM cars
            WHERE rented_state IN ('RENTED', 'AVAILABLE');
        """
        results = self.db_manager.execute_query(query)
        if results:
            print("Rented and Available Cars:")
            for row in results:
                print(f"ID: {row[0]}, Make: {row[1]}, Model: {row[2]}, Year: {row[3]}, rented_state: {row[4]}")
        else:
            print("No rented or available cars found.")
        return results
    # This method retrieves all users, printing their details, constructing a query to filter by user attributes.
    def get_all_users(self, filters=None):
        base_query = """
            SELECT id, name, email, username, state_of_account FROM users
        """
        final_sql, params = self.build_filtered_query(base_query, ['id', 'name', 'email', 'username', 'state_of_account'], filters = filters or {})
        results = self.db_manager.execute_query(final_sql, params)
        if results:
            print("All Users:")
            for row in results:
                print(f"ID: {row[0]}, Name: {row[1]}, Email: {row[2]}, Username: {row[3]}, State: {row[4]}")
        else:
            print("No users found.")
        return results
    # This method retrieves all cars, printing their details, constructing a query to filter by car attributes.
    def get_all_cars(self, filters=None):
        base_query = """
            SELECT * FROM cars
        """
        final_sql, params = self.build_filtered_query(base_query, ['id', 'make', 'model', 'year', 'rented_state'], filters = filters or {})
        results = self.db_manager.execute_query(final_sql, params)
        if results:
            print("All Cars:")
            for row in results:
                print(f"ID: {row[0]}, Make: {row[1]}, Model: {row[2]}, Year: {row[3]}, rented_state: {row[4]}")
        else:
            print("No cars found.")
        return results
    # This method retrieves all rentals, printing their details, constructing a query to filter by rental attributes.
    def get_all_rentals(self, filters=None):
        base_query = """
            SELECT * FROM car_renters
        """
        final_sql, params = self.build_filtered_query(base_query, ['id', 'user_id', 'car_id', 'rent_status'], filters = filters or {})
        results = self.db_manager.execute_query(final_sql, params)
        if results:
            print("All Rentals:")
            for row in results:
                print(f"ID: {row[0]}, User ID: {row[1]}, Car ID: {row[2]}, Rent Status: {row[3]}")
        else:
            print("No rentals found.")
        return results
    