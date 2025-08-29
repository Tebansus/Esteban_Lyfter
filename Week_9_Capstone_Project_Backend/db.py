from contextlib import contextmanager
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker, scoped_session

class PgManager:
    # Uses shared metadata and engine for all repositories
    # This class manages the connection to the PostgreSQL database
    # It initializes the connection parameters and creates a scoped session
    # Then, with the context manager, it provides a session scope for executing database operations
    def __init__(self, db_name, user, password, host, port=5432):
        self.db_url = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{db_name}"
        self.engine = create_engine(self.db_url)
        self.Session = scoped_session(sessionmaker(bind=self.engine))
        self.metadata = MetaData(schema="week_9_capstone_project")
        print("Connection created successfully")

    # Context manager function to handle session scope with the session functionality of SQLAlchemy ORM
    @contextmanager
    def session_scope(self):
        session = self.Session()
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    # Universal CRUD methods that work with any Table instance
    # These methods allow you to add, retrieve, edit, and delete entries in any table
    # Each repo calls these methods with the specific table instance and parameters
    # Taken from Week 6
    def add_table_entry(self, table, **kwargs):
        with self.session_scope() as sess:
            sess.execute(table.insert().values(**kwargs))
        print(f"Entry added to '{table.name}'")

    def get_table_entries(self, table):
        with self.session_scope() as sess:
            result = sess.execute(table.select()).fetchall()
        print(f"Entries retrieved from '{table.name}'")
        return result

    def edit_table_entry(self, table, entry_id, **kwargs):
        with self.session_scope() as sess:
            sess.execute(table.update().where(table.c.id == entry_id).values(**kwargs))
        print(f"Entry {entry_id} updated in '{table.name}'")

    def delete_table_entry(self, table, entry_id):
        with self.session_scope() as sess:
            sess.execute(table.delete().where(table.c.id == entry_id))
        print(f"Entry {entry_id} deleted from '{table.name}'")