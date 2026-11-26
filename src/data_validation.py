
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
PROCESSED_DIR = BASE_DIR / "data" / "processed"
validation_errors = []
validation_warnings = []


# Primary keys
primary_keys = {
    "olist_customers_dataset.csv": "customer_id",
    "olist_orders_dataset.csv": "order_id",
    "olist_products_dataset.csv": "product_id",
    "olist_sellers_dataset.csv": "seller_id",
    "product_category_name_translation.csv": "product_category_name"
}


# Composite keys
composite_keys = {
    "olist_order_reviews_dataset.csv": ["review_id", "order_id"],
    "olist_order_items_dataset.csv": ["order_id", "order_item_id"],
    "olist_order_payments_dataset.csv": ["order_id", "payment_sequential"]
}


# 1. Primary and Composite Key Validation
for file in sorted(PROCESSED_DIR.glob("*.csv")):

    if file.name == "quality_report.csv":
        continue

    print("\nValidating:", file.name)
    df = pd.read_csv(file)

    if file.name in primary_keys:

        key = primary_keys[file.name]

        null_count = df[key].isna().sum()
        duplicate_count = df[key].duplicated().sum()

        print("Primary key:", key)
        print("Null values:", null_count)
        print("Duplicate key values:", duplicate_count)

        if null_count > 0 or duplicate_count > 0:
            validation_errors.append(
                f"{file.name}: Primary key validation failed "
                f"(nulls={null_count}, duplicates={duplicate_count})"
            )

    elif file.name in composite_keys:

        keys = composite_keys[file.name]

        null_count = df[keys].isna().any(axis=1).sum()
        duplicate_count = df.duplicated(subset=keys).sum()

        print("Composite key:", keys)
        print("Rows with null key values:", null_count)
        print("Duplicate key combinations:", duplicate_count)

        if null_count > 0 or duplicate_count > 0:
            validation_errors.append(
                f"{file.name}: Composite key validation failed "
                f"(nulls={null_count}, duplicates={duplicate_count})"
            )

    else:
        print("No primary key defined.")


    # Review ID investigation
    if file.name == "olist_order_reviews_dataset.csv":

        duplicate_reviews = df[
            df["review_id"].duplicated(keep=False)
        ]

        review_id_counts = df["review_id"].value_counts()

        print("\nRows with repeated review_id:", len(duplicate_reviews))
        print("Review IDs appearing more than once:",
              (review_id_counts > 1).sum())

        print("Maximum occurrences of one review_id:",
              review_id_counts.max())

        print("\nReview ID occurrence distribution:")
        print(review_id_counts[review_id_counts > 1].value_counts().sort_index())

        duplicate_details = duplicate_reviews.groupby("review_id").agg(
            total_rows=("order_id", "size"),
            unique_orders=("order_id", "nunique"),
            unique_scores=("review_score", "nunique")
        )

        print("\nDuplicate review details:")
        print(duplicate_details.head(10))

        duplicate_pairs = df.duplicated(
            subset=["review_id", "order_id"]
        ).sum()

        print("Duplicate review_id + order_id pairs:", duplicate_pairs)


    # Geolocation investigation
    elif file.name == "olist_geolocation_dataset.csv":

        print("\nTotal rows:", len(df))

        print("Rows with repeated zip_code_prefix:",
              df["geolocation_zip_code_prefix"].duplicated().sum())

        duplicate_coordinates = df.duplicated(
            subset=[
                "geolocation_zip_code_prefix",
                "geolocation_lat",
                "geolocation_lng"
            ]
        ).sum()

        print("Repeated zip + coordinates combinations:",
              duplicate_coordinates)

        print("Complete duplicate records:", df.duplicated().sum())


# 2. Foreign Key Validation Function
def validate_foreign_key(
    child_df,
    parent_df,
    child_column,
    parent_column,
    relationship
):

    invalid = child_df[
        child_df[child_column].notna() &
        ~child_df[child_column].isin(parent_df[parent_column])
    ]

    print(f"\nForeign Key Validation: {relationship}")
    print("Invalid references:", len(invalid))
    print("Unique invalid values:", invalid[child_column].nunique())
    if len(invalid) > 0:
        validation_errors.append(
            f"{relationship}: {len(invalid)} invalid foreign key references"
        )


# 3. Load datasets required for foreign key validation
datasets = {
    "orders": "olist_orders_dataset.csv",
    "order_items": "olist_order_items_dataset.csv",
    "products": "olist_products_dataset.csv",
    "sellers": "olist_sellers_dataset.csv",
    "payments": "olist_order_payments_dataset.csv",
    "reviews": "olist_order_reviews_dataset.csv",
    "customers": "olist_customers_dataset.csv",
    "categories": "product_category_name_translation.csv"
}

data = {
    name: pd.read_csv(PROCESSED_DIR / filename)
    for name, filename in datasets.items()
}


# 4. Define foreign key relationships
foreign_keys = [
    ("order_items", "order_id", "orders", "order_id",
     "Order Items -> Orders"),

    ("order_items", "product_id", "products", "product_id",
     "Order Items -> Products"),

    ("order_items", "seller_id", "sellers", "seller_id",
     "Order Items -> Sellers"),

    ("payments", "order_id", "orders", "order_id",
     "Payments -> Orders"),

    ("reviews", "order_id", "orders", "order_id",
     "Reviews -> Orders"),

    ("orders", "customer_id", "customers", "customer_id",
     "Orders -> Customers")
]


# 5. Run foreign key validations
for child, child_col, parent, parent_col, label in foreign_keys:

    validate_foreign_key(
        data[child],
        data[parent],
        child_col,
        parent_col,
        label
    )


# 6. Product Category Translation Validation
products_df = data["products"]
categories_df = data["categories"]

invalid_categories = products_df[
    products_df["product_category_name"].notna() &
    ~products_df["product_category_name"].isin(
        categories_df["product_category_name"]
    )
]

print("\nForeign Key Validation: Products -> Category Translation")

if len(invalid_categories) > 0:
    validation_warnings.append(
        f"Product category translation gaps found: "
        f"{len(invalid_categories)} records"
    )

print("Unique invalid categories:",
      invalid_categories["product_category_name"].nunique())

print("Null category values:",
      products_df["product_category_name"].isna().sum())

print("\nInvalid category values:")
print(invalid_categories["product_category_name"].value_counts())

print("\nAffected product records:")
print(
    invalid_categories[
        ["product_id", "product_category_name"]
    ]
)

# Some product categories may not have a corresponding translation.
# These are mapping gaps, not necessarily invalid source categories.
# No records were modified.

# 7. Final Validation Summary

print("\n" + "=" * 60)
print("FINAL DATA VALIDATION SUMMARY")
print("=" * 60)

print("Total validation errors:", len(validation_errors))
print("Total validation warnings:", len(validation_warnings))

if validation_warnings:
    print("\nWarnings:")
    for warning in validation_warnings:
        print("-", warning)

if validation_errors:
    print("\nValidation Errors:")
    for error in validation_errors:
        print("-", error)

    raise ValueError("Data validation failed!")

print("\nData validation completed successfully!")