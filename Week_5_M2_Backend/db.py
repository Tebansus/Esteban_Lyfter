import psycopg2
# PG manager taken from the original class code, with some modifications.
class PgManager:
    def __init__(self, db_name, user, password, host, port=5432, options=None):
        self.db_name = db_name
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.options = options

        self.connection = self.create_connection(db_name, user, password, host, port, options)
        if self.connection:
            self.cursor = self.connection.cursor()
            print("Connection created succesfully")

    def create_connection(self, db_name, user, password, host, port, options):
        try:
            connection = psycopg2.connect(
                dbname=db_name,
                user=user,
                password=password,
                host=host,
                port=port,
                options=options
            )
            return connection
        except Exception as error:
            print("Error connecting to the database:", error)
            return None

    def close_connection(self):
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
        print("Connection closed")

    def execute_query(self, query, params=None):
        self.cursor.execute(query, params)
        self.connection.commit()

        # Revisamos si el query devolvió algo
        if self.cursor.description:
            results = self.cursor.fetchall()
            return results