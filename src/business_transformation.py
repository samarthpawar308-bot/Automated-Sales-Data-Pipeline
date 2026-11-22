
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
PROCESSED_DIR = BASE_DIR / "data" / "processed"

# Load order items dataset
items_df = pd.read_csv(
    PROCESSED_DIR / "olist_order_items_dataset.csv"
)

# Aggregate item-level data to order-level
order_items_agg = items_df.groupby("order_id").agg(
    total_items=("order_item_id", "count"),
    total_product_value=("price", "sum"),
    total_freight_value=("freight_value", "sum"),
    unique_products=("product_id", "nunique"),
    unique_sellers=("seller_id", "nunique")
).reset_index()

print("Order Items Aggregation:")
print(order_items_agg.head())

print("\nShape:", order_items_agg.shape)
print("Duplicate order_ids:", order_items_agg["order_id"].duplicated().sum())

print(
    "\nOriginal product value:",
    items_df["price"].sum()
)

print(
    "Aggregated product value:",
    order_items_agg["total_product_value"].sum()
)

print(
    "\nOriginal freight value:",
    items_df["freight_value"].sum()
)

print(
    "Aggregated freight value:",
    order_items_agg["total_freight_value"].sum()
)


# Load payments dataset
payments_df = pd.read_csv(
    PROCESSED_DIR / "olist_order_payments_dataset.csv"
)

# Aggregate payment data to order-level
payments_agg = payments_df.groupby("order_id").agg(
    total_payment_value=("payment_value", "sum"),
    payment_records=("payment_sequential", "count"),
    unique_payment_types=("payment_type", "nunique"),
    max_payment_installments=("payment_installments", "max")
).reset_index()

print("\nPayment Aggregation:")
print(payments_agg.head())

print("\nShape:", payments_agg.shape)

print(
    "Duplicate order_ids:",
    payments_agg["order_id"].duplicated().sum()
)

print(
    "\nOriginal payment value:",
    payments_df["payment_value"].sum()
)

print(
    "Aggregated payment value:",
    payments_agg["total_payment_value"].sum()
)


# Load reviews dataset
reviews_df = pd.read_csv(
    PROCESSED_DIR / "olist_order_reviews_dataset.csv"
)

# Aggregate review data to order-level
reviews_agg = reviews_df.groupby("order_id").agg(
    average_review_score=("review_score", "mean"),
    review_count=("review_id", "count")
).reset_index()

print("\nReview Aggregation:")
print(reviews_agg.head())

print("\nShape:", reviews_agg.shape)

print(
    "Duplicate order_ids:",
    reviews_agg["order_id"].duplicated().sum()
)

print(
    "\nOriginal review count:",
    reviews_df["review_id"].count()
)

print(
    "Aggregated review count:",
    reviews_agg["review_count"].sum()
)


# Load orders dataset
orders_df = pd.read_csv(
    PROCESSED_DIR / "olist_orders_dataset.csv"
)

print("\nOrders Dataset:")
print("Shape:", orders_df.shape)

print("\nOrder Status Distribution:")
print(orders_df["order_status"].value_counts())

print("\nMissing Values:")
print(orders_df.isnull().sum())

print("\nSample Records:")
print(orders_df.head())



# Merge aggregated datasets with orders

orders_analytics = orders_df.merge(
    order_items_agg,
    on="order_id",
    how="left",
    validate="one_to_one"
)

orders_analytics = orders_analytics.merge(
    payments_agg,
    on="order_id",
    how="left",
    validate="one_to_one"
)

orders_analytics = orders_analytics.merge(
    reviews_agg,
    on="order_id",
    how="left",
    validate="one_to_one"
)

print("\nMerged Orders Analytics Dataset:")

print("Shape:", orders_analytics.shape)

print(
    "Duplicate order IDs:",
    orders_analytics["order_id"].duplicated().sum()
)

print("\nMissing values after merging:")

print(
    orders_analytics[
        [
            "total_items",
            "total_product_value",
            "total_freight_value",
            "total_payment_value",
            "average_review_score",
            "review_count"
        ]
    ].isnull().sum()
)

print("\nSample records:")
print(orders_analytics.head())


# Investigate missing records by order status

missing_columns = [
    "total_items",
    "total_payment_value",
    "average_review_score"
]

for column in missing_columns:

    print(f"\nMissing {column} by order status:")

    missing_records = orders_analytics[
        orders_analytics[column].isnull()
    ]

    print(
        missing_records["order_status"].value_counts()
    )

# Inspect orders with missing payment information

print("\nOrder with missing payment information:")

print(
    orders_analytics[
        orders_analytics["total_payment_value"].isnull()
    ][
        ["order_id", "order_status", "order_purchase_timestamp"]
    ]
)

# Inspect orders without item records in unexpected statuses

unexpected_missing_items = orders_analytics[
    orders_analytics["total_items"].isnull()
    & orders_analytics["order_status"].isin(
        ["created", "invoiced", "shipped"]
    )
]

print("Orders without items in unexpected statuses:")
print(
    unexpected_missing_items[
        ["order_id", "order_status", "order_purchase_timestamp"]
    ]
)

print("\nTotal records:", len(unexpected_missing_items))

# Convert date columns to datetime

date_columns = [
    "order_purchase_timestamp",
    "order_delivered_customer_date",
    "order_estimated_delivery_date"
]

for column in date_columns:
    orders_analytics[column] = pd.to_datetime(
        orders_analytics[column],
        utc=True
    )

# Calculate actual delivery duration in days

orders_analytics["delivery_days"] = (
    orders_analytics["order_delivered_customer_date"]
    - orders_analytics["order_purchase_timestamp"]
).dt.total_seconds() / 86400

# Calculate delivery delay in days

orders_analytics["delivery_delay_days"] = (
    orders_analytics["order_delivered_customer_date"]
    - orders_analytics["order_estimated_delivery_date"]
).dt.total_seconds() / 86400

print("\nDelivery metrics:")
print(
    orders_analytics[
        [
            "order_status",
            "delivery_days",
            "delivery_delay_days"
        ]
    ].head(10)
)

# Validate delivery metrics

print("\nDelivery metrics validation:")

print(
    "Orders with delivery duration:",
    orders_analytics["delivery_days"].notnull().sum()
)

print(
    "Orders with delivery delay:",
    orders_analytics["delivery_delay_days"].notnull().sum()
)

print(
    "Non-delivered orders with delivery duration:",
    (
        (orders_analytics["order_status"] != "delivered")
        & orders_analytics["delivery_days"].notnull()
    ).sum()
)

print(
    "Negative delivery durations:",
    (orders_analytics["delivery_days"] < 0).sum()
)

print("\nDelivery duration summary:")
print(orders_analytics["delivery_days"].describe())

print("\nDelivery delay summary:")
print(orders_analytics["delivery_delay_days"].describe())

# Delivery Performance KPIs

delivered_orders = orders_analytics[
    orders_analytics["order_status"] == "delivered"
]

total_orders = len(orders_analytics)

total_delivered = len(delivered_orders)

average_delivery_days = delivered_orders["delivery_days"].mean()

on_time_orders = (
    delivered_orders["delivery_delay_days"] <= 0
).sum()

late_orders = (
    delivered_orders["delivery_delay_days"] > 0
).sum()

orders_with_delivery_data = delivered_orders[
    "delivery_delay_days"
].notnull().sum()

on_time_percentage = (
    on_time_orders / orders_with_delivery_data
) * 100

late_percentage = (
    late_orders / orders_with_delivery_data
) * 100

print("\n--- DELIVERY PERFORMANCE KPIs ---")

print("Total Orders:", total_orders)
print("Delivered Orders:", total_delivered)

print("Average Delivery Days:", round(average_delivery_days, 2))

print("On-time Orders:", on_time_orders)
print("Late Orders:", late_orders)

print("On-time Delivery %:", round(on_time_percentage, 2))
print("Late Delivery %:", round(late_percentage, 2))

# Load customer dataset

customers_df = pd.read_csv(
    PROCESSED_DIR / "olist_customers_dataset.csv"
)

# Select required customer columns

customer_data = customers_df[
    [
        "customer_id",
        "customer_unique_id",
        "customer_city",
        "customer_state"
    ]
]

# Merge customer information

orders_analytics = orders_analytics.merge(
    customer_data,
    on="customer_id",
    how="left",
    validate="many_to_one"
)

print("\nCustomer integration:")
print("Final shape:", orders_analytics.shape)
print("Duplicate order IDs:", orders_analytics["order_id"].duplicated().sum())

print("\nCustomer data sample:")
print(
    orders_analytics[
        ["order_id", "customer_unique_id", "customer_city", "customer_state"]
    ].head()
)

# Save final order-level analytical dataset

OUTPUT_FILE = PROCESSED_DIR / "order_level_analytics.csv"

orders_analytics.to_csv(
    OUTPUT_FILE,
    index=False
)

print("\nFinal analytical dataset saved successfully!")
print("File:", OUTPUT_FILE)
print("Shape:", orders_analytics.shape)