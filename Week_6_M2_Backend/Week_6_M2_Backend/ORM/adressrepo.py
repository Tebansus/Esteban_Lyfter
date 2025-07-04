class AddressRepo:
    def __init__(self, pg_manager):
        self.pg_manager = pg_manager
    # Function to add an address by calling the add_table_entry method from the PgManager class
    # It takes the user_id, street, city, and country as parameters and adds them to the address table
    def add_address(self, user_id, street, city, country):
        
        try:
            if user_id is None:
                raise ValueError("User ID cannot be None")
            self.pg_manager.add_table_entry(
                schema_name = "lyfter_week6",
                table_name = "address",
                user_id = user_id,
                street = street,
                city = city,
                country = country

            )
        except Exception as e:
            print(f"Error adding address: {e}")
            return 
        print("Address added successfully")
    # Function to modify an address by calling the edit_table_entry method from the PgManager class
    # It takes the address_id and optional parameters user_id, street, city, and country to update the address in the address table
    def modify_address(self, address_id, user_id=None, street=None, city=None, country=None):
        field_to_modify = {}
        if user_id:
            field_to_modify['user_id'] = user_id
        if street:
            field_to_modify['street'] = street
        if city:
            field_to_modify['city'] = city
        if country:
            field_to_modify['country'] = country
        
        try:
            self.pg_manager.edit_table_entry(
                schema_name = "lyfter_week6",
                table_name = "address",
                entry_id = address_id,
                **field_to_modify
            )
        except Exception as e:
            print(f"Error modifying address: {e}")
            return 
        print("Address modified successfully")
    # Function to delete an address by calling the delete_table_entry method from the PgManager class
    # It takes the address_id as a parameter and removes the address from the address table
    def delete_address(self, address_id):
        try:
            self.pg_manager.delete_table_entry(
                schema_name = "lyfter_week6",
                table_name = "address",
                entry_id = address_id
            )
        except Exception as e:
            print(f"Error deleting address: {e}")
            return 
        print("Address deleted successfully")
    # Function to check all addresses by retrieving and printing all addresses from the address table
    # It uses the get_table_entries method from the PgManager class
    def get_all_addresses(self):
        try:
            addresses = self.pg_manager.get_table_entries(
                schema_name = "lyfter_week6",
                table_name = "address"
            )
            if not addresses:
                print("No addresses found.")
                return
            for address in addresses:
                print(address)
        except Exception as e:
            print(f"Error retrieving addresses: {e}")
            return