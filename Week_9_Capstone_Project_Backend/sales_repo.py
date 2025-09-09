from sqlalchemy import Column, Integer, String, ForeignKey, Table, Numeric, DateTime
from datetime import datetime, timezone

class SalesRepo:
    def __init__(self, pg_manager):
        
        self.pg_manager = pg_manager

        # Define addresses, invoices, and invoice_items table structures
        self.addresses_table = Table(
            "addresses",
            self.pg_manager.metadata,
            Column("id", Integer, primary_key=True),
            Column("user_id", Integer, ForeignKey("week_9_capstone_project.users.id")),
            Column("address_line", String(100)),            
            Column("city", String(50)),
            Column("state", String(50)),
            Column("postal_code", String(20)),
            Column("country", String(50))
        )

        self.invoices_table = Table(
            "invoices",
            self.pg_manager.metadata,
            Column("id", Integer, primary_key=True),
            Column("user_id", Integer, ForeignKey("week_9_capstone_project.users.id")),
            Column("billing_address_id", Integer, ForeignKey("week_9_capstone_project.addresses.id")),            
            Column("total_price", Numeric(10, 2)),
            Column("created_at", DateTime, default=lambda: datetime.now(timezone.utc))
        )

        self.invoice_items_table = Table(
            "invoice_items",
            self.pg_manager.metadata,
            Column("id", Integer, primary_key=True),
            Column("invoice_id", Integer, ForeignKey("week_9_capstone_project.invoices.id")),
            Column("product_id", Integer, ForeignKey("week_9_capstone_project.products.id")),
            Column("quantity", Integer),
            Column("price_at_purchase", Numeric(10, 2))
        )

        # Ensure tables are created
        self.pg_manager.metadata.create_all(self.pg_manager.engine)

    # Address function to add a new address for a user
    def add_address(self, user_id, **kwargs):       
        self.pg_manager.add_table_entry(self.addresses_table, user_id=user_id, **kwargs)

    # Create Invoice function which uses the PG manager generic function to add an invoice
    def create_invoice(self, user_id, address_id, total):        
        self.pg_manager.add_table_entry(self.invoices_table,user_id=user_id,billing_address_id=address_id, total_price=total)
    # Add invoice item function to add an item to an invoice using the cross-table
    def add_invoice_item(self, invoice_id, product_id, quantity, price):        
        self.pg_manager.add_table_entry(self.invoice_items_table,invoice_id=invoice_id,product_id=product_id,quantity=quantity,price_at_purchase=price)
    # Get invoice with items function to retrieve an invoice and its items
    def get_invoice_with_items(self, invoice_id):       
        with self.pg_manager.session_scope() as sess:
            invoice = sess.execute(self.invoices_table.select().where(self.invoices_table.c.id == invoice_id)).fetchone()
            items = sess.execute(self.invoice_items_table.select().where(self.invoice_items_table.c.invoice_id == invoice_id)).fetchall()
        return invoice, items