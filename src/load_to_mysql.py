
import pandas as pd
from sqlalchemy.types import VARCHAR, DOUBLE, INTEGER
from db_config import get_database_engine

# 1. Read CSV
df = pd.read_csv(
    "data/processed/order_level_analytics.csv"
)

# 2. Convert timestamp columns
date_columns = [
    "order_purchase_timestamp",
    "order_approved_at",
    "order_delivered_carrier_date",
    "order_delivered_customer_date",
    "order_estimated_delivery_date"
]

for col in date_columns:
    df[col] = pd.to_datetime(df[col], utc=True).dt.tz_localize(None)

# 3. Define MySQL column types
dtype = {}

text_columns = [
    "order_id", "customer_id", "order_status",
    "customer_unique_id", "customer_city", "customer_state"
]

for col in text_columns:
    dtype[col] = VARCHAR(255)

for col in date_columns:
    dtype[col] = DATETIME()

numeric_columns = df.select_dtypes(include="number").columns

for col in numeric_columns:
    dtype[col] = DOUBLE()

engine = get_database_engine()

# 5. Load data
df.to_sql(
    name="order_level_analytics",
    con=engine,
    if_exists="replace",
    index=False,
    dtype=dtype,
    chunksize=5000,
    method="multi"
)

print("Data imported successfully!")

# 6. Verify
with engine.connect() as connection:
    from sqlalchemy import text

    count = connection.execute(
        text("SELECT COUNT(*) FROM order_level_analytics")
    ).scalar()

    print("Total records:", count)

engine.dispose()
