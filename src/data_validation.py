import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
PROCESSED_DIR = BASE_DIR / "data" / "processed"

#RAW_DIR = BASE_DIR / "data" / "raw"

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


for file in PROCESSED_DIR.glob("*.csv"):

    if file.name == "quality_report.csv":
        continue

    print("\nValidating:", file.name)

    df = pd.read_csv(file)

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

        print("Rows with repeated review_id:", len(duplicate_reviews))

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

        print("Rows with repeated zip_code_prefix:",
            df["geolocation_zip_code_prefix"].duplicated().sum())

        duplicate_coordinates = df.duplicated(
        subset=[
            "geolocation_zip_code_prefix",
            "geolocation_lat",
            "geolocation_lng"
        ]
            ).sum()

        print("Rows with repeated zip + coordinates combinations:",
            duplicate_coordinates)
        
        print("Complete duplicate records:",
            df.duplicated().sum())

# Foreign Key Validation

orders_df = pd.read_csv(
    PROCESSED_DIR / "olist_orders_dataset.csv"
)

order_items_df = pd.read_csv(
    PROCESSED_DIR / "olist_order_items_dataset.csv"
)

invalid_orders = order_items_df[
    order_items_df["order_id"].notna() &
    ~order_items_df["order_id"].isin(orders_df["order_id"])
]

null_order_ids = order_items_df["order_id"].isnull().sum()

print("\nForeign Key Validation: Order Items -> Orders")

print("Invalid order_id references:", len(invalid_orders))
print("Unique invalid order_ids:", invalid_orders["order_id"].nunique())
print("Null order_id values:", null_order_ids)

products_df = pd.read_csv(
    PROCESSED_DIR / "olist_products_dataset.csv"
)

invalid_products = order_items_df[
    order_items_df["product_id"].notna() &
    ~order_items_df["product_id"].isin(products_df["product_id"])
]

null_product_ids = order_items_df["product_id"].isnull().sum()

print("\nForeign Key Validation: Order Items -> Products")
print("Invalid product_id references:", len(invalid_products))
print("Unique invalid product_ids:", invalid_products["product_id"].nunique())
print("Null product_id values:", null_product_ids)

sellers_df = pd.read_csv(
    PROCESSED_DIR / "olist_sellers_dataset.csv"
)

invalid_sellers = order_items_df[
    order_items_df["seller_id"].notna() &
    ~order_items_df["seller_id"].isin(sellers_df["seller_id"])
]

print("\nForeign Key Validation: Order Items -> Sellers")
print("Invalid seller_id references:", len(invalid_sellers))
print("Unique invalid seller_ids:", invalid_sellers["seller_id"].nunique())
print("Null seller_id values:", order_items_df["seller_id"].isnull().sum())

payments_df = pd.read_csv(
    PROCESSED_DIR / "olist_order_payments_dataset.csv"
)

invalid_payments = payments_df[
    payments_df["order_id"].notna() &
    ~payments_df["order_id"].isin(orders_df["order_id"])
]

print("\nForeign Key Validation: Payments -> Orders")
print("Invalid order_id references:", len(invalid_payments))
print("Unique invalid order_ids:", invalid_payments["order_id"].nunique())
print("Null order_id values:", payments_df["order_id"].isnull().sum())

reviews_df = pd.read_csv(
    PROCESSED_DIR / "olist_order_reviews_dataset.csv"
)

invalid_reviews = reviews_df[
    reviews_df["order_id"].notna() &
    ~reviews_df["order_id"].isin(orders_df["order_id"])
]

print("\nForeign Key Validation: Reviews -> Orders")
print("Invalid order_id references:", len(invalid_reviews))
print("Unique invalid order_ids:", invalid_reviews["order_id"].nunique())
print("Null order_id values:", reviews_df["order_id"].isnull().sum())

customers_df = pd.read_csv(
    PROCESSED_DIR / "olist_customers_dataset.csv"
)

invalid_customers = orders_df[
    orders_df["customer_id"].notna() &
    ~orders_df["customer_id"].isin(customers_df["customer_id"])
]

print("\nForeign Key Validation: Orders -> Customers")
print("Invalid customer_id references:", len(invalid_customers))
print("Unique invalid customer_ids:", invalid_customers["customer_id"].nunique())
print("Null customer_id values:", orders_df["customer_id"].isnull().sum())

products_df = pd.read_csv(
    PROCESSED_DIR / "olist_products_dataset.csv"
)

categories_df = pd.read_csv(
    PROCESSED_DIR / "product_category_name_translation.csv"
)

invalid_categories = products_df[
    products_df["product_category_name"].notna() &
    ~products_df["product_category_name"].isin(
        categories_df["product_category_name"]
    )
]

print("\nInvalid category values:")

print(
    invalid_categories["product_category_name"]
    .value_counts()
)

print("\nAffected product records:")

print(
    invalid_categories[
        ["product_id", "product_category_name"]
    ]
)

print("\nForeign Key Validation: Products -> Category Translation")
print("Invalid category references:", len(invalid_categories))
print("Unique invalid categories:",
      invalid_categories["product_category_name"].nunique())
print("Null category values:",
      products_df["product_category_name"].isnull().sum())

# 13 products belong to 2 categories not found
# in the category translation mapping.
# These may be valid source categories with missing translations.
# No records were modified.