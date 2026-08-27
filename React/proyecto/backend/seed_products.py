import os
import json
from db import PgManager
from product_repo import ProductRepo
from dotenv import load_dotenv

load_dotenv()

pg_manager = PgManager(
    db_name=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    host=os.getenv("DB_HOST")
)

# Import all repos to populate metadata
from user_repo import UserRepo
from cart_repo import CartRepo
from sales_repo import SalesRepo
from refund_repo import RefundRepo

UserRepo(pg_manager)
CartRepo(pg_manager)
SalesRepo(pg_manager)
RefundRepo(pg_manager)
product_repo = ProductRepo(pg_manager)

pg_manager.metadata.drop_all(pg_manager.engine)
pg_manager.metadata.create_all(pg_manager.engine)

# Read products.json
with open("../src/data/products.json", "r", encoding="utf-8") as f:
    products = json.load(f)

for p in products:
    product_repo.add_product(
        nombre=p["nombre"],
        descripcion=p.get("descripcion", ""),
        precio=p["precio"],
        categoria=p.get("categoria", ""),
        imagen=p.get("imagen", ""),
        stock=p.get("stock", 0)
    )

print("Successfully seeded products into the database!")
