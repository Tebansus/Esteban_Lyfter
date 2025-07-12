from sqlalchemy import Column, Integer, String, Table, ForeignKey

class CarRepo:
    def __init__(self, pg_manager):
        self.pg_manager = pg_manager
        # declare the table once
        # This table is for storing cars linked to users
        # If table already exists, it will not be recreated
        self.table = Table(
            "cars",
            self.pg_manager.metadata,
            Column("id", Integer, primary_key=True),
            Column("user_id", Integer, ForeignKey("lyfter_orm.users.id"), nullable=True),
            Column("car_model", String(50), nullable=False),
            Column("car_make", String(50), nullable=False),
            Column("car_year", Integer, nullable=False),
            extend_existing=True
        )
        self.pg_manager.metadata.create_all(self.pg_manager.engine)
    # CRUD functions
    # Add_car - adds a new car to the database by calling the add_table_entry method
    def add_car(self, user_id, car_model, car_make, car_year):
        self.pg_manager.add_table_entry(
            self.table,
            user_id=user_id,
            car_model=car_model,
            car_make=car_make,
            car_year=car_year
        )
    # Modify_car: modifies an existing car by calling the edit_table_entry method
    def modify_car(self, car_id, **fields):
        self.pg_manager.edit_table_entry(self.table, car_id, **fields)
    # Delete_car: deletes a car from the database by calling the delete_table_entry method
    def delete_car(self, car_id):
        self.pg_manager.delete_table_entry(self.table, car_id)
    # List_cars: retrieves and prints all cars from the database
    def list_cars(self):
        for row in self.pg_manager.get_table_entries(self.table):
            print(row)
    # Link_car_to_user: links a car to a user by modifying the user_id field of the car
    def link_car_to_user(self, car_id, user_id):
        self.modify_car(car_id, user_id=user_id)