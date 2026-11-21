import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
PROCESSED_DIR = BASE_DIR / "data" / "processed"

for file in PROCESSED_DIR.glob("*.csv"):

    if file.name == "quality_report.csv":
        continue

    print("\nValidating:", file.name)

    df = pd.read_csv(file)

    primary_keys = {
    "olist_customers_dataset.csv": "customer_id",
    "olist_geolocation_dataset.csv": None,
    "olist_orders_dataset.csv": "order_id",
    "olist_order_items_dataset.csv": None,
    "olist_order_payments_dataset.csv": None,
    "olist_order_reviews_dataset.csv": None,
    "olist_products_dataset.csv": "product_id",
    "olist_sellers_dataset.csv": "seller_id",
    "product_category_name_translation.csv": "product_category_name"
    }

    composite_keys = {
    "olist_order_reviews_dataset.csv": ["review_id", "order_id"],
    "olist_order_items_dataset.csv": ["order_id", "order_item_id"],
    "olist_order_payments_dataset.csv": ["order_id", "payment_sequential"]
    }

    key = primary_keys.get(file.name)

    if key is None:

        if file.name in composite_keys:
            key_columns = composite_keys[file.name]

            null_count = df[key_columns].isnull().any(axis=1).sum()
            duplicate_count = df.duplicated(subset=key_columns).sum()

            print("Composite key:", key_columns)
            print("Rows with null key values:", null_count)
            print("Duplicate key combinations:", duplicate_count)

        else:
            print("Primary key not defined yet")

    else:
        null_count = df[key].isnull().sum()
        duplicate_count = df[key].duplicated().sum()

        print("Primary key:", key)
        print("Null values:", null_count)
        print("Duplicate key values:", duplicate_count)
    
    if file.name == "olist_order_reviews_dataset.csv":

        duplicate_reviews = df[
        df["review_id"].duplicated(keep=False)
        ]

        print("Duplicate review rows:", len(duplicate_reviews))

        print(duplicate_reviews[
            ["review_id", "order_id", "review_score"]
        ].head(10))

        review_id_counts = df["review_id"].value_counts()

        print("Review IDs appearing more than once:",
            (review_id_counts > 1).sum())

        print("Maximum occurrences of one review_id:",
            review_id_counts.max())

        print(review_id_counts[review_id_counts > 1].value_counts().sort_index())

        duplicate_review_details = df[
        df["review_id"].duplicated(keep=False)
        ].groupby("review_id").agg(
        total_rows=("order_id", "size"),
        unique_orders=("order_id", "nunique"),
        unique_scores=("review_score", "nunique")
        )

        print(duplicate_review_details.head(10))

        duplicate_pairs = df.duplicated(
        subset=["review_id", "order_id"]
        ).sum()

        print("Duplicate review_id + order_id pairs:", duplicate_pairs)

    if file.name == "olist_geolocation_dataset.csv":

        print("Total rows:", len(df))

        print("Duplicate zip_code_prefix:",
          df["geolocation_zip_code_prefix"].duplicated().sum())

        duplicate_coordinates = df.duplicated(
        subset=[
            "geolocation_zip_code_prefix",
            "geolocation_lat",
            "geolocation_lng"
        ]
            ).sum()

        print("Duplicate zip + coordinates combinations:",
            duplicate_coordinates)

        print("Complete duplicate records:",
            df.duplicated().sum())
