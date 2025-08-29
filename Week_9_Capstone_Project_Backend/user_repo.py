# Add 'insert' to your imports from sqlalchemy
from sqlalchemy import Column, ForeignKey, Integer, String, Table, DateTime, select, insert
from datetime import datetime, timezone

class UserRepo:
    def __init__(self, pg_manager):
        self.pg_manager = pg_manager

        #  Define the roles table
        self.roles_table = Table(
            "roles",
            self.pg_manager.metadata,
            Column("id", Integer, primary_key=True),
            Column("name", String(20), unique=True)
        )

        # Define the users table
        self.users_table = Table(
            "users",
            self.pg_manager.metadata,
            Column("id", Integer, primary_key=True),
            Column("username", String(30), unique=True),
            Column("email", String(100), unique=True),
            Column("password", String),            
            Column("role_id", Integer, ForeignKey("week_9_capstone_project.roles.id")),
            Column("created_at", DateTime, default=lambda: datetime.now(timezone.utc))
        )
        
        
        self.pg_manager.metadata.create_all(self.pg_manager.engine)
        
        # Call the seeding method after tables are created
        self._seed_roles()

    # Seeding method to always add default roles
    def _seed_roles(self):
       
        default_roles = [{'id': 1, 'name': 'user'},{'id': 2, 'name': 'admin'}]
        with self.pg_manager.session_scope() as sess:
            for role_data in default_roles:
                # Check if a role with this id already exists
                role_exists = sess.query(self.roles_table).filter_by(id=role_data['id']).first()                
                # If it doesn't exist, insert it
                if not role_exists:
                    # Insert and commit if the roles do not exist
                    stmt = insert(self.roles_table).values(id=role_data['id'], name=role_data['name'])
                    sess.execute(stmt)
                    print(f"✅ Default role '{role_data['name']}' created.")
            sess.commit() 

    # Crud functions for the user
    def add_user(self, username, email, password, role_id):
        self.pg_manager.add_table_entry(self.users_table,username=username,email=email,password=password,role_id=role_id)
    # Function to find the user by the user's credentials, mostly to be used by the login endpoint
    def find_user_by_credentials(self, username, password_hash):        
        with self.pg_manager.session_scope() as sess:
            # Join users table with roles table to get the role name            
            join = self.users_table.join(self.roles_table, self.users_table.c.role_id == self.roles_table.c.id)
            
            # Construct a statement to select the user's ID and role name
            stmt = select(self.users_table.c.id, self.roles_table.c.name.label('role_name')).select_from(join).where(self.users_table.c.username == username,self.users_table.c.password == password_hash)
             # Execute the statement and fetch one result
            result = sess.execute(stmt).fetchone()        
        return result

    # Modify user with kwargs by calling the generic function in pg_manager
    def modify_user(self, user_id, **fields):
        self.pg_manager.edit_table_entry(self.users_table, user_id, **fields)
    # Delete user by ID by calling the generic function in pg_manager
    def delete_user(self, user_id):
        self.pg_manager.delete_table_entry(self.users_table, user_id)
    # List all users by calling the generic function in pg_manager
    def list_users(self):
        for row in self.pg_manager.get_table_entries(self.users_table):
            print(row)
            
    # Role functions
    # Add role using the generic function in pg_manager
    def add_role(self, name):
        self.pg_manager.add_table_entry(self.roles_table, name=name)
    # Modify role with kwargs by calling the generic function in pg_manager
    def modify_role(self, role_id, **fields):
        self.pg_manager.edit_table_entry(self.roles_table, role_id, **fields)
    # Delete role by ID by calling the generic function in pg_manager
    def delete_role(self, role_id):
        self.pg_manager.delete_table_entry(self.roles_table, role_id)
    # List all roles by calling the generic function in pg_manager
    def list_roles(self):
        for row in self.pg_manager.get_table_entries(self.roles_table):
            print(row)