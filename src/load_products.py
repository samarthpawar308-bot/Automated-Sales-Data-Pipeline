import pandas as pd
from sqlalchemy.types import VARCHAR, DOUBLE, INTEGER
from db_config import get_database_engine

df = pd.read_csv("data/raw/olist_products_dataset.csv")

dtype = {
    "product_id": VARCHAR(32),
    "product_category_name": VARCHAR(100),
    "product_name_lenght": INTEGER(),
    "product_description_lenght": INTEGER(),
    "product_photos_qty": INTEGER(),
    "product_weight_g": DOUBLE(),
    "product_length_cm": DOUBLE(),
    "product_height_cm": DOUBLE(),
    "product_width_cm": DOUBLE()
}

engine = get_database_engine()

df.to_sql(
    name="products",
    con=engine,
    if_exists="replace",
    index=False,
    dtype=dtype,
    chunksize=5000
)

print("Products imported successfully!")
print("Rows loaded:", len(df))

engine.dispose()
