
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

RAW_DIR = BASE_DIR / "data" / "raw"
PROCESSED_DIR = BASE_DIR / "data" / "processed"

PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

# Date columns present in Olist datasets
date_columns = {
    "olist_orders_dataset.csv": [
        "order_purchase_timestamp",
        "order_approved_at",
        "order_delivered_carrier_date",
        "order_delivered_customer_date",
        "order_estimated_delivery_date"
    ],
    "olist_order_items_dataset.csv": [
        "shipping_limit_date"
    ],
    "olist_order_reviews_dataset.csv": [
        "review_creation_date",
        "review_answer_timestamp"
    ]
}

# Candidate unique keys for validation
key_columns = {
    "olist_orders_dataset.csv": ["order_id"],
    "olist_customers_dataset.csv": ["customer_id"],
    "olist_products_dataset.csv": ["product_id"],
    "olist_sellers_dataset.csv": ["seller_id"],
    "olist_order_items_dataset.csv": [
        "order_id", "order_item_id"
    ],
    "olist_order_payments_dataset.csv": [
        "order_id", "payment_sequential"
    ],
    "olist_order_reviews_dataset.csv": ["review_id"]
}

quality_report = []

for file in RAW_DIR.glob("*.csv"):

    print("\nProcessing:", file.name)

    df = pd.read_csv(file)

    original_rows = len(df)

    text_columns = df.select_dtypes(
        include=["object", "string"]
    ).columns

    for col in text_columns:
        df[col] = df[col].astype("string").str.strip()


    df = df.replace(r"^\s*$", pd.NA, regex=True)

    # 3. Remove exact duplicate rows
    exact_duplicates = df.duplicated().sum()
    df = df.drop_duplicates()

    # 4. Convert known date columns
    invalid_dates = 0

    for col in date_columns.get(file.name, []):
        if col in df.columns:
            original_values = df[col].notna().sum()

            df[col] = pd.to_datetime(
                df[col],
                errors="coerce",
                utc=True
            )

            invalid_dates += original_values - df[col].notna().sum()

    # 5. Check candidate key duplicates
    key_duplicate_rows = 0
    keys = key_columns.get(file.name, [])

    if keys and all(col in df.columns for col in keys):
        key_duplicate_rows = df.duplicated(
            subset=keys
        ).sum()

    # 6. Save cleaned file
    output_file = PROCESSED_DIR / file.name
    df.to_csv(output_file, index=False)

    # 7. Record quality information
    quality_report.append({
        "file": file.name,
        "original_rows": original_rows,
        "final_rows": len(df),
        "exact_duplicates_removed": exact_duplicates,
        "key_duplicate_rows": key_duplicate_rows,
        "invalid_dates": invalid_dates,
        "missing_values": int(df.isna().sum().sum())
    })

    print("Original rows:", original_rows)
    print("Final rows:", len(df))
    print("Exact duplicates removed:", exact_duplicates)
    print("Candidate key duplicate rows:", key_duplicate_rows)
    print("Invalid dates:", invalid_dates)

# Save quality report
report = pd.DataFrame(quality_report)

report.to_csv(
    PROCESSED_DIR / "quality_report.csv",
    index=False
)

print("\nCleaning completed!")
print(report)
