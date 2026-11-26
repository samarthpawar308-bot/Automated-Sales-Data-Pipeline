
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
PROCESSED_DIR = BASE_DIR / "data" / "processed"

for file in sorted(PROCESSED_DIR.glob("*.csv")):

    if file.name == "quality_report.csv":
        continue

    print("\nAnalyzing:", file.name)
    df = pd.read_csv(file)

    # Review dataset analysis
    if file.name == "olist_order_reviews_dataset.csv":

        both_missing = (
            df["review_comment_title"].isna() &
            df["review_comment_message"].isna()
        )

        print("Total reviews:", len(df))
        print("Missing review scores:", df["review_score"].isna().sum())
        print("Both comments missing:", both_missing.sum())

        print(
            "Ratings present despite missing comments:",
            df.loc[both_missing, "review_score"].notna().sum()
        )

    # Orders dataset analysis
    elif file.name == "olist_orders_dataset.csv":

        print("\nOrder status distribution:")
        print(df["order_status"].value_counts())

        missing_delivery = df["order_delivered_customer_date"].isna()

        missing_status = missing_delivery.groupby(df["order_status"]).sum()
        print("\nMissing delivery dates by order status:")
        print(missing_status)

        delivered_missing = df[
            (df["order_status"] == "delivered") &
            missing_delivery
        ]

        print("\nDelivered orders with missing delivery dates:")
        print(delivered_missing[
            [
                "order_id",
                "order_status",
                "order_delivered_customer_date",
                "order_delivered_carrier_date",
                "order_estimated_delivery_date"
            ]
        ])

        missing_approval = df[df["order_approved_at"].isna()]

        print("\nMissing approval timestamps:", len(missing_approval))
        print(missing_approval["order_status"].value_counts())

        delivered_missing_approval = df[
            (df["order_status"] == "delivered") &
            df["order_approved_at"].isna()
        ]

        print("\nDelivered orders with missing approval timestamps:")
        print(delivered_missing_approval[
            [
                "order_id",
                "order_purchase_timestamp",
                "order_approved_at",
                "order_delivered_customer_date"
            ]
        ])

    # Products dataset analysis
    elif file.name == "olist_products_dataset.csv":

        missing_products = df[df["product_category_name"].isna()]

        print("\nProducts with missing category:", len(missing_products))

        descriptive_cols = [
            "product_category_name",
            "product_name_lenght",
            "product_description_lenght",
            "product_photos_qty"
        ]

        print(missing_products[
            ["product_id"] + descriptive_cols
        ].head())

        all_missing = missing_products[descriptive_cols].isna().all(axis=1)

        print("Products with all 4 descriptive fields missing:", all_missing.sum())

        dimension_cols = [
            "product_weight_g",
            "product_length_cm",
            "product_height_cm",
            "product_width_cm"
        ]

        missing_dimensions = df[
            df[dimension_cols].isna().any(axis=1)
        ]

        print("Products with missing dimensions:", len(missing_dimensions))

        print(missing_dimensions[
            ["product_id", "product_category_name"] + dimension_cols
        ].to_string(index=False))

    # Overall missing-value analysis
    missing_values = df.isna().sum()
    missing_values = missing_values[missing_values > 0]

    missing_percentage = (missing_values / len(df)) * 100

    print("\nMissing value percentage:")
    print(missing_percentage)
