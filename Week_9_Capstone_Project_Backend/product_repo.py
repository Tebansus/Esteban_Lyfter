from sqlalchemy import Column, Integer, String, Numeric, DateTime, Table
from datetime import datetime, timezone
# Product Repo Class, idea taken from Week 6. 
class ProductRepo:
    def __init__(self, pg_manager):        
        self.pg_manager = pg_manager
        self.table = Table(
            "products",
            self.pg_manager.metadata,
            Column("id", Integer, primary_key=True),
            Column("name", String(100), nullable=False),
            Column("description", String),
            Column("price", Numeric(10, 2), nullable=False),
            Column("stock_quantity", Integer, default=0),
            Column("created_at", DateTime, default=lambda: datetime.now(timezone.utc)),
            Column("updated_at", DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
        )
        self.pg_manager.metadata.create_all(self.pg_manager.engine)
    # Add product using the pg manager generic function
    def add_product(self, name, description, price, stock_quantity):       
        self.pg_manager.add_table_entry(self.table,name=name,description=description, price=price,stock_quantity=stock_quantity)
    # Modify product using the pg manager generic function
    def modify_product(self, product_id, **fields):        
        self.pg_manager.edit_table_entry(self.table, product_id, **fields)
    # adjust stock by using the session scope to update the stock quantity in the table
    def adjust_stock(self, product_id, quantity_delta):     
        with self.pg_manager.session_scope() as sess:
            sess.execute(self.table.update().where(self.table.c.id == product_id).values(stock_quantity=self.table.c.stock_quantity + quantity_delta))
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