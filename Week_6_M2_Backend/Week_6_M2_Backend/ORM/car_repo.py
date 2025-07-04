
class CarRepository:
    def __init__(self, pg_manager):
        self.pg_manager = pg_manager
    
    # Function to add cars by calling the add_table_entry method from the PgManager class
    # It takes the user_id, car_model, car_make, and car_year as parameters and adds them to the cars table
    def add_cars(self, user_id, car_model, car_make,car_year):
        try:  
            
            self.pg_manager.add_table_entry(
                schema_name="lyfter_week6",
                table_name="cars",
                user_id=user_id,
                car_model=car_model,
                car_make = car_make,
                car_year=car_year
            )
            print(f"Car '{car_model}' added successfully.")
        except Exception as e:
            print(f"Error adding car: {e}")
            return
    # Function to modify cars by calling the edit_table_entry method from the PgManager class
    # It takes the car_id and optional parameters user_id, car_model, car_make, and car_year to update the car in the cars table
    def modify_car(self, car_id, user_id=None, car_model=None, car_make=None, car_year=None):
        updated_fields = {}
        if user_id:
            updated_fields['user_id'] = user_id
        if car_model:
            updated_fields['car_model'] = car_model
        if car_make:
            updated_fields['car_make'] = car_make
        if car_year:
            updated_fields['car_year'] = car_year

        try:
            self.pg_manager.edit_table_entry(
                schema_name="lyfter_week6",
                table_name="cars",
                entry_id=car_id,
                **updated_fields
            )
            print(f"Car '{car_id}' modified successfully.")
        except Exception as e:
            print(f"Error modifying car: {e}")
            return
    # Function to delete a car by calling the delete_table_entry method from the PgManager class
    # It takes the car_id as a parameter and removes the car from the cars table
    def delete_car(self, car_id):
        try:
            self.pg_manager.delete_table_entry(
                schema_name="lyfter_week6",
                table_name="cars",
                entry_id=car_id
            )
            print(f"Car '{car_id}' deleted successfully.")
        except Exception as e:
            print(f"Error deleting car: {e}")
            return
    # Function to check all cars by retrieving and printing all cars from the cars table
    # it uses the get_table_entries method from the PgManager class
    # If no cars are found, it prints a message indicating that no cars were found
    def check_all_cars(self):
        try:
            cars = self.pg_manager.get_table_entries(
                schema_name="lyfter_week6",
                table_name="cars"
            )
            if not cars:
                print("No cars found.")
                return
            for car in cars:
                print(car)
        except Exception as e:
            print(f"Error retrieving cars: {e}")
            return
    # Function to link a car to a user by calling the edit_table_entry method from the PgManager class
    # It takes the car_id and user_id as parameters and updates the user_id in the cars table
    # This allows a car to be associated with a specific user
    def link_car_to_user(self, car_id, user_id):
        try:
            self.pg_manager.edit_table_entry(
                schema_name="lyfter_week6",
                table_name="cars",
                entry_id=car_id,
                user_id=user_id
            )
            print(f"Car '{car_id}' linked to user '{user_id}' successfully.")
        except Exception as e:
            print(f"Error linking car to user: {e}")
            return