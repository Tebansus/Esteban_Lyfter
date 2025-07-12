from sqlalchemy import Column, Integer, String, Table, ForeignKey

class AddressRepo:
    def __init__(self, pg_manager):
        self.pg_manager = pg_manager
        # Declare the table once
        # This table is for storing addresses linked to users
        self.table = Table(
            "address",
            self.pg_manager.metadata,
            Column("id", Integer, primary_key=True),
            Column("user_id", Integer, ForeignKey("lyfter_orm.users.id"), nullable=False),
            Column("street", String(100), nullable=False),
            Column("city", String(50), nullable=False),
            Column("country", String(50), nullable=False),
            extend_existing=True
        )
        self.pg_manager.metadata.create_all(self.pg_manager.engine)
    # CRUD functions, first add_address function that adds a new address to the database
    def add_address(self, user_id, street, city, country):
        if user_id is None:
            raise ValueError("User ID cannot be None")
        self.pg_manager.add_table_entry(
            self.table,
            user_id=user_id,
            street=street,
            city=city,
            country=country
        )
    # second, modify_address function that modifies an existing address
    # It takes the address_id and any fields to modify
    def modify_address(self, address_id, **fields):
        self.pg_manager.edit_table_entry(self.table, address_id, **fields)
    # third, delete_address function that deletes an address from the database
    # It takes the address_id as a parameter
    def delete_address(self, address_id):
        self.pg_manager.delete_table_entry(self.table, address_id)
    # Finally, list_addresses function that retrieves and prints all addresses from the database
    def list_addresses(self):
        for row in self.pg_manager.get_table_entries(self.table):
            print(row)