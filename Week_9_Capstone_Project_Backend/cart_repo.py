from sqlalchemy import Column, Integer, String, ForeignKey, Table, DateTime
from datetime import datetime, timezone

class CartRepo:
    def __init__(self, pg_manager):
      
        self.pg_manager = pg_manager
        
        self.cart_items_table = Table(
            "cart_items",
            self.pg_manager.metadata,
            Column("id", Integer, primary_key=True),
            Column("cart_id", Integer, ForeignKey("week_9_capstone_project.carts.id")),
            Column("product_id", Integer, ForeignKey("week_9_capstone_project.products.id")),
            Column("quantity", Integer, default=1)
        )

        # Define the carts and cart_items table structures, logic taken from week 6 by defining the table inside the repository class constructor
        self.carts_table = Table(
            "carts",
            self.pg_manager.metadata,
            Column("id", Integer, primary_key=True),
            Column("user_id", Integer, ForeignKey("week_9_capstone_project.users.id")),
            Column("status", String(20), default='active'),  
            Column("created_at", DateTime, default=lambda: datetime.now(timezone.utc)),
            Column("updated_at", DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
        )

        
        
        # Create tables
        self.pg_manager.metadata.create_all(self.pg_manager.engine)

    # Cart functions
    # Create cart function
    def create_cart(self, user_id):        
        self.pg_manager.add_table_entry(self.carts_table, user_id=user_id, status='active')
    # Function to retrieve active cart for a given user
    def get_active_cart_by_user(self, user_id):
        
        with self.pg_manager.session_scope() as sess:
            result = sess.execute(self.carts_table.select().where(self.carts_table.c.user_id == user_id,self.carts_table.c.status == 'active')).fetchone()
        return result
    # Function to adjust the cart status to signify completion or cancellation
    def update_cart_status(self, cart_id, status):        
        self.pg_manager.edit_table_entry(self.carts_table, cart_id, status=status)


    # Function to add item to a specific cart
    def add_item_to_cart(self, cart_id, product_id, quantity):        
        self.pg_manager.add_table_entry(self.cart_items_table, cart_id=cart_id, product_id=product_id, quantity=quantity)
    # Function to update the quantity of an item in the cart
    def update_item_quantity(self, item_id, quantity):        
        self.pg_manager.edit_table_entry(self.cart_items_table, item_id, quantity=quantity)
    # Function to remove an item from the cart
    def remove_item_from_cart(self, item_id):       
        self.pg_manager.delete_table_entry(self.cart_items_table, item_id)
    # Function to retrieve all items in a specific cart
    def get_cart_items(self, cart_id):      
        with self.pg_manager.session_scope() as sess:
            result = sess.execute(self.cart_items_table.select().where(self.cart_items_table.c.cart_id == cart_id)).fetchall()
        return result