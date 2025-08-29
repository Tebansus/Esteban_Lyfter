from sqlalchemy import Column, Integer, String, ForeignKey, Table, DateTime
from datetime import datetime, timezone

class RefundRepo:
    def __init__(self, pg_manager):
        
        self.pg_manager = pg_manager

        # Define the refunds table structure
        self.refunds_table = Table(
            "refunds",
            self.pg_manager.metadata,
            Column("id", Integer, primary_key=True),
            Column("invoice_id", Integer, ForeignKey("week_9_capstone_project.invoices.id")),
            Column("product_id", Integer, ForeignKey("week_9_capstone_project.products.id")),
            Column("quantity", Integer),
            Column("reason", String),
            Column("refund_date", DateTime, default=lambda: datetime.now(timezone.utc))
        )
        
        
        self.pg_manager.metadata.create_all(self.pg_manager.engine)
    # Create refund function by using the PGmanager generic function to add an entry
    def create_refund(self, invoice_id, product_id, quantity, reason):        
        self.pg_manager.add_table_entry(self.refunds_table,invoice_id=invoice_id,product_id=product_id,quantity=quantity,reason=reason)
    # Get refunds for a specific invoice function that pulls the refunds associated with that invoice
    def get_refunds_for_invoice(self, invoice_id):        
        with self.pg_manager.session_scope() as sess:
            result = sess.execute(self.refunds_table.select().where(self.refunds_table.c.invoice_id == invoice_id)).fetchall()
        return result