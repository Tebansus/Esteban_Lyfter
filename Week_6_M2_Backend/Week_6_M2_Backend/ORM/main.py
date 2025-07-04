from sqlalchemy import create_engine, Column, Integer, String, Table, MetaData, ForeignKey
from sqlalchemy.schema import CreateSchema
from db import PgManager
from users import User_functions
from car_repo import CarRepository
from adressrepo import AddressRepo
def main():
    # Database connection 
    db_name = "lyfter_test"
    user =   "postgres"
    password = "passparapostgress"
    host = "localhost"
    port = 5432
    # Table definitions for sqlalchemy ORM 
    user_columns= [
        Column('id', Integer, primary_key=True),
        Column('name', String(50), nullable=False),
        Column('email', String(100), nullable=False, unique=True),
        Column('password', String(100), nullable=False)
    ]
    car_columns = [
        Column('id', Integer, primary_key=True),
        Column('user_id', Integer, ForeignKey('lyfter_week6.users.id'), nullable=True),
        Column('car_model', String(50), nullable=False),
        Column('car_make', String(50), nullable=False),
        Column('car_year', Integer, nullable=False)
    ]
    adress_columns = [
        Column('id', Integer, primary_key=True),
        Column('user_id', Integer, ForeignKey('lyfter_week6.users.id'), nullable=False),
        Column('street', String(100), nullable=False),
        Column('city', String(50), nullable=False),
        Column('country', String(50), nullable=False)
    ]
    # Create an instance of PgManager
    pg_manager = PgManager(db_name, user, password, host, port)
    # create the 3 tables in the database
    pg_manager.create_table("lyfter_week6", "users", user_columns)
    pg_manager.create_table("lyfter_week6", "cars", car_columns)
    pg_manager.create_table("lyfter_week6", "address", adress_columns)
    # create user repository to manage users
    users_repo = User_functions(pg_manager)
    # Add a user, modify a user, delete a user, and check all users
    users_repo.add_users("John Doe", "aliuyy@gmail.com","12345")
    users_repo.add_users("John Doey", "aliusda@gmail.com","12345")
    users_repo.add_users("Jane Doe", "ssss@gmail.com","12345")
    users_repo.modif_user(1, name="Johnyyy_doey")
    users_repo.delete_user(3)
    users_repo.check_all_users()
    # Add a car, modify a car, delete a car, and check all cars.
    car_repo = CarRepository(pg_manager)
    car_repo.add_cars(1, "Model S", "Tesla", 2020)
    car_repo.add_cars(2, "Yuan Plus", "BYD", 2023)
    car_repo.modify_car(1, car_model="Model X", car_year=2021)
    car_repo.delete_car(2)   
    car_repo.check_all_cars()
    
    # Add an address, modify an address, delete an address, and check all addresses
    address_repo = AddressRepo(pg_manager)
    address_repo.add_address(1, "123 St", "Springfield", "USA")
    address_repo.add_address(2, "Infiernillo", "Alajuela", "Costa Rica")
    address_repo.modify_address(1, street="456 St", city="Los Santos")
    address_repo.delete_address(2)
    address_repo.get_all_addresses()
    pg_manager.close_connection()
if __name__ == "__main__":
    main()
    # Close the database connection
