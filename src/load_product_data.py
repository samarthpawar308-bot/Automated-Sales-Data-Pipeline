
import pandas as pd
from sqlalchemy.types import VARCHAR, DOUBLE, INTEGER
from db_config import get_database_engine

# Read order items dataset
df = pd.read_csv("data/raw/olist_order_items_dataset.csv")

# Convert date column
df["shipping_limit_date"] = pd.to_datetime(
    df["shipping_limit_date"],
    errors="coerce"
)

# Define MySQL data types
dtype = {
    "order_id": VARCHAR(32),
    "order_item_id": INTEGER(),
    "product_id": VARCHAR(32),
    "seller_id": VARCHAR(32),
    "shipping_limit_date": DATETIME(),
    "price": DOUBLE(),
    "freight_value": DOUBLE()
}

engine = get_database_engine()

# Load data
df.to_sql(
    name="order_items",
    con=engine,
    if_exists="replace",
    index=False,
    dtype=dtype,
    chunksize=5000
)

print("Order items imported successfully!")
print("Rows loaded:", len(df))

engine.dispose()