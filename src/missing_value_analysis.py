import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

PROCESSED_DIR = BASE_DIR / "data" / "processed"

for file in PROCESSED_DIR.glob("*.csv"):
    if file.name == "quality_report.csv":
        continue

    print("\n Analyzing : ", file.name)
    df = pd.read_csv(file)

    if file.name == "olist_order_reviews_dataset.csv":

        print("Total reviews:", len(df))

        print("Missing review scores:", df["review_score"].isnull().sum())

        both_missing = (
            df["review_comment_title"].isnull() &
            df["review_comment_message"].isnull()
        )

        print("Both comments missing:", both_missing.sum())

        print("Ratings present despite missing comments:",
            df.loc[both_missing, "review_score"].notnull().sum())

        #Conclusion of this is that customers can submit a rating without leaving a feedback

    if file.name == "olist_orders_dataset.csv":
        print(df['order_status'].value_counts())

        missing_status = df.groupby('order_status')['order_delivered_customer_date'].apply(lambda x : x.isnull().sum())
        print(missing_status) #missing dates of delivered orders according to each order status

        #investigating furthur for missing delivery dates for orders that were deliverd
        delivered_missing = df[(df["order_status"] == "delivered") & (df['order_delivered_customer_date'].isnull())]
        print(delivered_missing[["order_id", "order_status", "order_delivered_customer_date", "order_delivered_carrier_date", "order_estimated_delivery_date"]])


        missing_approval = df[df["order_approved_at"].isnull()]

        print("Missing approval timestamps:", len(missing_approval))

        print(missing_approval["order_status"].value_counts())

        delivered_missing_approval = df[
        (df["order_status"] == "delivered") &
        (df["order_approved_at"].isnull())
        ]   

        print(delivered_missing_approval[
        ["order_id", "order_purchase_timestamp",
        "order_approved_at", "order_delivered_customer_date"]
        ])

        # Missing values were investigated in the order timestamp columns.
        # Most missing values appear to be related to order statuses.
        # However, some delivered orders have missing approval or delivery timestamps,
        # which require further validation. No data was modified.

    #Products dataset
    if file.name == "olist_products_dataset.csv":

        missing_products = df[df["product_category_name"].isnull()]

        print("Products with missing category:", len(missing_products))

        print(missing_products[
            ["product_id", "product_category_name",
            "product_name_lenght", "product_description_lenght",
            "product_photos_qty"]
        ].head())

        descriptive_cols = [
        "product_category_name",
        "product_name_lenght",
        "product_description_lenght",
        "product_photos_qty"
        ]

        all_missing = missing_products[descriptive_cols].isnull().all(axis=1)

        print("Products with all 4 fields missing:", all_missing.sum())

        dimension_cols = [
        "product_weight_g",
        "product_length_cm",
        "product_height_cm",
        "product_width_cm"
        ]

        missing_dimensions = df[
        df[dimension_cols].isnull().any(axis=1)
        ]

        print("Products with missing dimensions:", len(missing_dimensions))

        print(missing_dimensions[
            ["product_id", "product_category_name"] + dimension_cols
        ])

        print(missing_dimensions[
        ["product_id", "product_weight_g",
        "product_length_cm", "product_height_cm",
        "product_width_cm"]
        ].to_string(index=False))

        # 610 products have all four descriptive fields missing.
        # 2 products have all four physical dimension fields missing.
        # These missing values require further investigation before handling.
        # No records were modified.

    missing_value = df.isnull().sum()
    missing_value = missing_value[missing_value > 0]

    #calculating missing value percentage for each dataset
    total_rows = len(df)
    missing_value_percentage = (missing_value/ total_rows) * 100
    print(missing_value_percentage)