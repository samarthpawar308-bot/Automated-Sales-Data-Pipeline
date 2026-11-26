import pandas as pd
from sqlalchemy.types import VARCHAR, DOUBLE, INTEGER
from db_config import get_database_engine


df = pd.read_csv("data/raw/olist_order_payments_dataset.csv")

print("Dataset shape:", df.shape)
print(df.head())

dtype = {
    "order_id": VARCHAR(32),
    "payment_sequential": INTEGER(),
    "payment_type": VARCHAR(50),
    "payment_installments": INTEGER(),
    "payment_value": DOUBLE()
}

engine = get_database_engine()

df.to_sql(
    name="order_payments",
    con=engine,
    if_exists="replace",
    index=False,
    dtype=dtype,
    chunksize=5000
)

print("Payment data imported successfully!")
print("Rows loaded:", len(df))

engine.dispose()
