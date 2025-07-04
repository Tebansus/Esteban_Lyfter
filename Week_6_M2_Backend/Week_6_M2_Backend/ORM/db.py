from sqlalchemy import create_engine, Column, Integer, String, Table, MetaData, ForeignKey
from sqlalchemy.schema import CreateSchema
from sqlalchemy.orm import sessionmaker, scoped_session

class PgManager:
    # Constructor to initialize the database connection, it also links the schema and starts the engine, session, and metadata
    # The metadata is shared across all tables created in this class
    def __init__(self, db_name, user, password, host, port=5432):
        self.db_url = f"postgresql://{user}:{password}@{host}:{port}/{db_name}"
        self.engine = create_engine(self.db_url)
        self.Session = scoped_session(sessionmaker(bind=self.engine))        
        self.metadata = MetaData(schema="lyfter_week6")
        print("Connection created successfully")
    # Method to close the connection, it removes the session
    def close_connection(self):
        self.Session.remove()
        print("Connection closed")
    # Method to create tble if it does not exist, it takes the schema name, table name, and columns as parameters
    def create_table(self, schema_name, table_name, columns):       
        table = Table(table_name, self.metadata, *columns)      
        self.metadata.create_all(self.engine)
        print(f"Table '{table_name}' created successfully in schema '{schema_name}'")
        
    # Methods to add a table entry with the insert smt, by calling the table contents with the engine and metadata
    def add_table_entry(self, schema_name, table_name, **kwargs):
        session = self.Session()
        
        table = Table(table_name, self.metadata, autoload_with=self.engine)
        insert_stmt = table.insert().values(**kwargs)
        session.execute(insert_stmt)
        session.commit()
        print(f"Entry added to table '{table_name}' in schema '{schema_name}'")
        session.close()
    # Methods to get all entries from a table, it takes the schema name and table name as parameters, then autoloads the table 
    # with the engine and metadata, and executes a select statement to retrieve all entries
    def get_table_entries(self, schema_name, table_name):
        session = self.Session()        
        table = Table(table_name, self.metadata, autoload_with=self.engine)
        select_stmt = table.select()
        result = session.execute(select_stmt).fetchall()
        session.close()
        print(f"Entries retrieved from table '{table_name}' in schema '{schema_name}'")
        return result
    # Methods to edit a table entry, it takes the schema name, table name, and entry id as parameters, then autoloads the table
    # with the engine and metadata, and executes an update statement to modify the entry with the
    def edit_table_entry(self, schema_name, table_name, entry_id, **kwargs):
        session = self.Session()       
        table = Table(table_name, self.metadata, autoload_with=self.engine)
        update_stmt = table.update().where(table.c.id == entry_id).values(**kwargs)
        session.execute(update_stmt)
        session.commit()
        print(f"Entry with ID '{entry_id}' updated in table '{table_name}' in schema '{schema_name}'")
        session.close()
    # Methods to delete a table entry, it takes the schema name, table name, and entry id as parameters, then autoloads the table
    # with the engine and metadata, and executes a delete statement to remove the entry with the
    def delete_table_entry(self, schema_name, table_name, entry_id):
        session = self.Session()        
        table = Table(table_name, self.metadata, autoload_with=self.engine)
        delete_stmt = table.delete().where(table.c.id == entry_id)
        session.execute(delete_stmt)
        session.commit()
        print(f"Entry with ID '{entry_id}' deleted from table '{table_name}' in schema '{schema_name}'")
        session.close()