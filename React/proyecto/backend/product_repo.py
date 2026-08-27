from sqlalchemy import Column, Integer, String, Numeric, DateTime, Table
from datetime import datetime, timezone
# Product Repo Class
class ProductRepo:
    def __init__(self, pg_manager):        
        self.pg_manager = pg_manager
        self.table = Table(
            "products",
            self.pg_manager.metadata,
            Column("id", Integer, primary_key=True),
            Column("nombre", String(100), nullable=False),
            Column("descripcion", String),
            Column("precio", Numeric(10, 2), nullable=False),
            Column("categoria", String(100)),
            Column("imagen", String),
            Column("stock", Integer, default=0),
            Column("created_at", DateTime, default=lambda: datetime.now(timezone.utc)),
            Column("updated_at", DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
        )
        self.pg_manager.metadata.create_all(self.pg_manager.engine)
    # Add product using the pg manager generic function
    def add_product(self, nombre, descripcion, precio, categoria, imagen, stock):       
        self.pg_manager.add_table_entry(self.table,nombre=nombre,descripcion=descripcion, precio=precio,categoria=categoria,imagen=imagen,stock=stock)
    # Modify product using the pg manager generic function
    def modify_product(self, product_id, **fields):        
        self.pg_manager.edit_table_entry(self.table, product_id, **fields)
    # adjust stock by using the session scope to update the stock quantity in the table
    def adjust_stock(self, product_id, quantity_delta):     
        with self.pg_manager.session_scope() as sess:
            sess.execute(self.table.update().where(self.table.c.id == product_id).values(stock=self.table.c.stock + quantity_delta))
        print(f"Stock for product {product_id} adjusted by {quantity_delta}")
    #use the PG manager function to delete a product
    def delete_product(self, product_id):        
        self.pg_manager.delete_table_entry(self.table, product_id)
    # list products using the pg manager generic function
    def list_products(self):        
        return self.pg_manager.get_table_entries(self.table)
    # get product by id by using the session scope to execute an SQL alchemy query to retrieve a product by its ID
    def get_product_by_id(self, product_id):       
        with self.pg_manager.session_scope() as sess:
            result = sess.execute(self.table.select().where(self.table.c.id == product_id)).fetchone()
        return result
