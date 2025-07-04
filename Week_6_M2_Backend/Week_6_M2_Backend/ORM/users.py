class User_functions:
    def __init__(self, PgManager):
        self.pg_manager = PgManager
    # User function to add users by calling the add_table_entry method from the PgManager class
    # It takes the name, email, and password as parameters and adds them to the users table
    def add_users(self, name, email, password):
        try: 
            self.pg_manager.add_table_entry(
                schema_name="lyfter_week6",
                table_name="users",
                name=name,
                email=email,
                password=password
            )
        except Exception as e:
            print(f"Error adding user: {e}")
            return
        print(f"User '{name}' added successfully.")
    # function to modify users by calling the edit_table_entry method from the PgManager class
    # It takes the user_id and optional parameters name, email, and password to update the user in the users table

    def modif_user(self, user_id, name=None, email=None, password=None):
        updated_fields = {}
        if name:
            updated_fields['name'] = name
        if email:
            updated_fields['email'] = email
        if password:
            updated_fields['password'] = password

        try:
            self.pg_manager.edit_table_entry(
                schema_name="lyfter_week6",
                table_name="users",
                entry_id=user_id,
                **updated_fields
            )
        except Exception as e:
            print(f"Error modifying user: {e}")
            return
        print(f"User '{user_id}' modified successfully.")
    # Delete user function to remove a user by calling the delete_table_entry method from the PgManager class
    def delete_user(self, user_id):
        try:
            self.pg_manager.delete_table_entry(
                schema_name="lyfter_week6",
                table_name="users",
                entry_id=user_id
            )
        except Exception as e:
            print(f"Error deleting user: {e}")
            return
    # Check all users function to retrieve and print all users from the users table
    def check_all_users(self):
        try:
            users = self.pg_manager.get_table_entries(
                schema_name="lyfter_week6",
                table_name="users"
            )
            if not users:
                print("No users found.")
                return
            for user in users:
                print(user)
        except Exception as e:
            print(f"Error retrieving users: {e}")
            return
        print("Users retrieved successfully.")