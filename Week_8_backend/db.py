from sqlalchemy import create_engine
from sqlalchemy import MetaData
from sqlalchemy import Table, Column, Integer, String, ForeignKey, Numeric
from sqlalchemy import insert, select

metadata_obj = MetaData(schema="lyfter_week_7")
# added the role column to the user table to manage user roles
user_table = Table(
    "users",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("username", String(30), unique=True),
    Column("password", String),
    Column("role", String(15), nullable=False, default="user")  #  user | admin
)
product_table = Table(
    "products",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("name", String(30)),
    Column("price", Integer),
    Column("Date_of_Entry", String(30)),
    Column("quantity", Integer)
)
# Added invoice table to manage user purchases
invoice_table = Table(
    "invoices",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("user_id", Integer, ForeignKey("lyfter_week_7.users.id")),
    Column("product_id", Integer, ForeignKey("lyfter_week_7.products.id")),
    Column("product_name", String(30)),
    Column("unit_price", Numeric),
    Column("quantity", Integer),
    Column("total", Numeric)
)

class DB_Manager:
    def __init__(self):
        self.engine = create_engine('') # Insert your own database connection string here
        metadata_obj.create_all(self.engine)
    # CRUD operations for users, first we need to insert a user
    # this method will return the id of the inserted user
    # if the user already exists, it will return None
    def insert_user(self, username, password, role="user"):
        stmt = (insert(user_table).returning(user_table.c.id).values(username=username, password=password, role=role))
        with self.engine.connect() as conn:
            user_id = conn.execute(stmt).scalar()
            conn.commit()
        return user_id
    # this method will return the user row if the user exists
    # if the user does not exist, it will return None
    def get_user(self, username, password):
        stmt = select(user_table).where(user_table.c.username == username).where(user_table.c.password == password)
        with self.engine.connect() as conn:
            result = conn.execute(stmt)
            users = result.all()

            if(len(users)==0):
                return None
            else:
                return users[0]
    # this method will return the user row if the user exists by id
    # if the user does not exist, it will return None
    # this is used to get the user information after authentication
    # to show the user information in the /me endpoint
    def get_user_by_id(self, id):
        stmt = select(user_table).where(user_table.c.id == id)
        with self.engine.connect() as conn:
            result = conn.execute(stmt)
            users = result.all()
            if(len(users)==0):
                return None
            else:
                return users[0]
    #Crud operations for products
    # First, we need to insert a product. This method will return the id of the inserted product. It inserts the product into the database via the SQLAlchemy engine.
    def insert_product(self, name, price, date_of_entry, quantity):
        stmt = insert(product_table).values(name=name, price=price, Date_of_Entry=date_of_entry, quantity=quantity)
        with self.engine.connect() as conn:
            result = conn.execute(stmt)
            conn.commit()
        return result.inserted_primary_key
    # This method will return all the products in the database
    # it will return a list of rows, each row is a product
    # It uses the SQLAlchemy engine to execute a select statement on the product table.
    def list_products(self):
        stmt = select(product_table)
        with self.engine.connect() as conn:
            rows = conn.execute(stmt).all()
        return rows
    # This method will return a product by its id
    # if the product does not exist, it will return None
    # It uses the SQLAlchemy engine to execute a select statement on the product table.
    def get_product(self, product_id):
        stmt = select(product_table).where(product_table.c.id == product_id)
        with self.engine.connect() as conn:
            result = conn.execute(stmt)
            products = result.all()
            if(len(products)==0):
                return None
            else:
                return products[0]
    # This method will update a product by its id
    # it will return the number of rows affected
    # if the product does not exist, it will return 0
    # It uses the SQLAlchemy engine to execute an update statement on the product table.
    def edit_product(self, id, **kwargs):
        stmt = product_table.update().where(product_table.c.id == id).values(**kwargs)
        with self.engine.connect() as conn:
            result = conn.execute(stmt)
            conn.commit()
        return result.rowcount
    # This method will delete a product by its id
    # it will return the number of rows affected
    # if the product does not exist, it will return 0
    def delete_product(self, id):
        stmt = product_table.delete().where(product_table.c.id == id)
        with self.engine.connect() as conn:
            result = conn.execute(stmt)
            conn.commit()
        return result.rowcount
    # Finally, we need to adjust the stock of a product. This function will increase or decrease the stock of a product by a given delta value.
    # It will return the number of rows affected.
    def adjust_stock(self, id, delta):
        stmt = (product_table.update().where(product_table.c.id == id).values(quantity=product_table.c.quantity + delta))
        with self.engine.connect() as conn:
            result = conn.execute(stmt)
            conn.commit()
        return result.rowcount
    
    # CRUD operations for invoices, this method will insert an invoice into the database
    # it will return the id of the inserted invoice
    
    def insert_invoice(self, user_id, product_id, product_name, unit_price, quantity):
        total = unit_price * quantity
        stmt = (insert(invoice_table).returning(invoice_table.c.id).values(user_id=user_id, product_id=product_id,product_name=product_name, unit_price=unit_price,quantity=quantity,total=total))
        with self.engine.connect() as conn:
            result = conn.execute(stmt)
            conn.commit()
        return result.scalar()
    # This method will return all the invoices for a user
    def get_invoices_by_user(self, user_id):
        stmt = select(invoice_table).where(invoice_table.c.user_id == user_id)
        with self.engine.connect() as conn:
            rows = conn.execute(stmt).all()
        return rows