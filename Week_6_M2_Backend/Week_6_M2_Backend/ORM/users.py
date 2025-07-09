from sqlalchemy import Column, Integer, String, Table

class UserRepo:
    def __init__(self, pg_manager):
        self.pg_manager = pg_manager

        # Declare the table once
        self.table = Table(
            "users",
            self.pg_manager.metadata,
            Column("id", Integer, primary_key=True),
            Column("name", String(50), nullable=False),
            Column("email", String(100), nullable=False, unique=True),
            Column("password", String(100), nullable=False),
            extend_existing=True          # important for multiple runs
        )
        # Create it in the database (does nothing if it already exists)
        self.pg_manager.metadata.create_all(self.pg_manager.engine)

    # CRUD functions
    # Add_user - adds a new user to the database by calling the add_table_entry method
    def add_user(self, name, email, password):
        self.pg_manager.add_table_entry(
            self.table,
            name=name,
            email=email,
            password=password
        )
    # Modify_user - modifies an existing user by calling the edit_table_entry method
    def modify_user(self, user_id, **fields):
        self.pg_manager.edit_table_entry(self.table, user_id, **fields)
    # Delete_user - deletes a user from the database by calling the delete_table_entry method
    def delete_user(self, user_id):
        self.pg_manager.delete_table_entry(self.table, user_id)
    # List_users - retrieves and prints all users from the database
    def list_users(self):
        for row in self.pg_manager.get_table_entries(self.table):
            print(row)