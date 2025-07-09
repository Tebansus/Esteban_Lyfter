from db import PgManager
from users import UserRepo
from car_repo import CarRepo
from adressrepo import AddressRepo

def main():
    # DB connection data
    pg_manager = PgManager(
        db_name="postgres",
        user="postgres",
        password="Estebanessupercool22",
        host="localhost",
        port=5432
    )

    # Repositories (tables are created automatically)
    user_repo    = UserRepo(pg_manager)
    car_repo     = CarRepo(pg_manager)
    address_repo = AddressRepo(pg_manager)

    # User operations, it adds 3 users, modifies one, deletes another, and lists all
    user_repo.add_user("John Doe",  "aliuyy@gmail.com", "12345")
    user_repo.add_user("John Doey", "aliusda@gmail.com", "12345")
    user_repo.add_user("Jane Doe",  "ssss@gmail.com",   "12345")

    user_repo.modify_user(1, name="Johnyyy_doey")
    user_repo.delete_user(3)
    user_repo.list_users()

    # car operations, it adds 2 cars, modifies one, deletes another, and lists all
    car_repo.add_car(1, "Model S",   "Tesla", 2020)
    car_repo.add_car(2, "Yuan Plus", "BYD",   2023)
    car_repo.modify_car(1, car_model="Model X", car_year=2021)
    car_repo.delete_car(2)
    car_repo.list_cars()

    # address operations, it adds 2 addresses, modifies one, deletes another, and lists all
    address_repo.add_address(1, "123 St",     "Springfield", "USA")
    address_repo.add_address(2, "Infiernillo","Alajuela",    "Costa Rica")
    address_repo.modify_address(1, street="456 St", city="Los Santos")
    address_repo.delete_address(2)
    address_repo.list_addresses()

if __name__ == "__main__":
    main()