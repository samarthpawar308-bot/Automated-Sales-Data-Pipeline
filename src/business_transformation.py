

import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
PROCESSED_DIR = BASE_DIR / "data" / "processed"


# 1. Load datasets
items_df = pd.read_csv(PROCESSED_DIR / "olist_order_items_dataset.csv")
payments_df = pd.read_csv(PROCESSED_DIR / "olist_order_payments_dataset.csv")
reviews_df = pd.read_csv(PROCESSED_DIR / "olist_order_reviews_dataset.csv")
orders_df = pd.read_csv(PROCESSED_DIR / "olist_orders_dataset.csv")


# 2. Generic order-level aggregation function
def aggregate_by_order(df, aggregations, dataset_name, reconciliation=None):

    aggregated_df = df.groupby("order_id").agg(
        **aggregations
    ).reset_index()

    print(f"\n{dataset_name} Aggregation:")
    print(aggregated_df.head())
    print("Shape:", aggregated_df.shape)
    print("Duplicate order_ids:", aggregated_df["order_id"].duplicated().sum())

    if reconciliation:
        print("\nAggregation reconciliation:")

        for source_col, aggregate_col in reconciliation:
            print(f"Original {source_col}:", df[source_col].sum())
            print(f"Aggregated {aggregate_col}:",
                  aggregated_df[aggregate_col].sum())

    return aggregated_df


# 3. Aggregate order items
order_items_agg = aggregate_by_order(
    items_df,
    {
        "total_items": ("order_item_id", "count"),
        "total_product_value": ("price", "sum"),
        "total_freight_value": ("freight_value", "sum"),
        "unique_products": ("product_id", "nunique"),
        "unique_sellers": ("seller_id", "nunique")
    },
    "Order Items",
    [
        ("price", "total_product_value"),
        ("freight_value", "total_freight_value")
    ]
)


# 4. Aggregate payments
payments_agg = aggregate_by_order(
    payments_df,
    {
        "total_payment_value": ("payment_value", "sum"),
        "payment_records": ("payment_sequential", "count"),
        "unique_payment_types": ("payment_type", "nunique"),
        "max_payment_installments": ("payment_installments", "max")
    },
    "Payment",
    [
        ("payment_value", "total_payment_value")
    ]
)


# 5. Aggregate reviews
reviews_agg = aggregate_by_order(
    reviews_df,
    {
        "average_review_score": ("review_score", "mean"),
        "review_count": ("review_id", "count")
    },
    "Review",
    [
        ("review_id", "review_count")
    ]
)


# 6. Inspect orders dataset
print("\nOrders Dataset:")
print("Shape:", orders_df.shape)

print("\nOrder Status Distribution:")
print(orders_df["order_status"].value_counts())

print("\nMissing Values:")
print(orders_df.isna().sum())

print("\nSample Records:")
print(orders_df.head())


# 7. Merge aggregated datasets with orders
orders_analytics = orders_df.copy()

for aggregated_df in [
    order_items_agg,
    payments_agg,
    reviews_agg
]:
    orders_analytics = orders_analytics.merge(
        aggregated_df,
        on="order_id",
        how="left",
        validate="one_to_one"
    )


print("\nMerged Orders Analytics Dataset:")
print("Shape:", orders_analytics.shape)

print("Duplicate order IDs:",
      orders_analytics["order_id"].duplicated().sum())

missing_columns = [
    "total_items",
    "total_product_value",
    "total_freight_value",
    "total_payment_value",
    "average_review_score",
    "review_count"
]

print("\nMissing values after merging:")
print(orders_analytics[missing_columns].isna().sum())

print("\nSample records:")
print(orders_analytics.head())


# 8. Investigate missing records by order status
for column in [
    "total_items",
    "total_payment_value",
    "average_review_score"
]:
    missing_records = orders_analytics[
        orders_analytics[column].isna()
    ]

    print(f"\nMissing {column} by order status:")
    print(missing_records["order_status"].value_counts())


# Inspect orders with missing payment information
print("\nOrders with missing payment information:")

print(
    orders_analytics.loc[
        orders_analytics["total_payment_value"].isna(),
        ["order_id", "order_status", "order_purchase_timestamp"]
    ]
)


# Inspect orders without items in selected unexpected statuses
unexpected_missing_items = orders_analytics[
    orders_analytics["total_items"].isna() &
    orders_analytics["order_status"].isin(
        ["created", "invoiced", "shipped"]
    )
]

print("\nOrders without items in unexpected statuses:")

print(
    unexpected_missing_items[
        ["order_id", "order_status", "order_purchase_timestamp"]
    ]
)

print("Total records:", len(unexpected_missing_items))


# 9. Convert date columns
date_columns = [
    "order_purchase_timestamp",
    "order_delivered_customer_date",
    "order_estimated_delivery_date"
]

orders_analytics[date_columns] = orders_analytics[date_columns].apply(
    lambda col: pd.to_datetime(col, utc=True)
)


# 10. Calculate delivery metrics
orders_analytics["delivery_days"] = (
    orders_analytics["order_delivered_customer_date"]
    - orders_analytics["order_purchase_timestamp"]
).dt.total_seconds() / 86400

orders_analytics["delivery_delay_days"] = (
    orders_analytics["order_delivered_customer_date"]
    - orders_analytics["order_estimated_delivery_date"]
).dt.total_seconds() / 86400


print("\nDelivery Metrics:")
print(
    orders_analytics[
        ["order_status", "delivery_days", "delivery_delay_days"]
    ].head(10)
)


# 11. Validate delivery metrics
print("\nDelivery Metrics Validation:")

print("Orders with delivery duration:",
      orders_analytics["delivery_days"].notna().sum())

print("Orders with delivery delay:",
      orders_analytics["delivery_delay_days"].notna().sum())

print(
    "Non-delivered orders with delivery duration:",
    (
        (orders_analytics["order_status"] != "delivered") &
        orders_analytics["delivery_days"].notna()
    ).sum()
)

print("Negative delivery durations:",
      (orders_analytics["delivery_days"] < 0).sum())

print("\nDelivery Duration Summary:")
print(orders_analytics["delivery_days"].describe())

print("\nDelivery Delay Summary:")
print(orders_analytics["delivery_delay_days"].describe())


# 12. Delivery Performance KPIs
delivered_orders = orders_analytics[
    orders_analytics["order_status"] == "delivered"
]

total_orders = len(orders_analytics)
total_delivered = len(delivered_orders)

average_delivery_days = delivered_orders["delivery_days"].mean()

delivery_data = delivered_orders["delivery_delay_days"].dropna()

on_time_orders = (delivery_data <= 0).sum()
late_orders = (delivery_data > 0).sum()

orders_with_delivery_data = len(delivery_data)

on_time_percentage = (
    on_time_orders / orders_with_delivery_data * 100
    if orders_with_delivery_data else 0
)

late_percentage = (
    late_orders / orders_with_delivery_data * 100
    if orders_with_delivery_data else 0
)


print("\n--- DELIVERY PERFORMANCE KPIs ---")

print("Total Orders:", total_orders)
print("Delivered Orders:", total_delivered)
print("Average Delivery Days:", round(average_delivery_days, 2))

print("On-time Orders:", on_time_orders)
print("Late Orders:", late_orders)

print("On-time Delivery %:", round(on_time_percentage, 2))
print("Late Delivery %:", round(late_percentage, 2))


# 13. Integrate customer information
customers_df = pd.read_csv(
    PROCESSED_DIR / "olist_customers_dataset.csv"
)

customer_data = customers_df[
    [
        "customer_id",
        "customer_unique_id",
        "customer_city",
        "customer_state"
    ]
]

orders_analytics = orders_analytics.merge(
    customer_data,
    on="customer_id",
    how="left",
    validate="many_to_one"
)


print("\nCustomer Integration:")
print("Final Shape:", orders_analytics.shape)

print("Duplicate order IDs:",
      orders_analytics["order_id"].duplicated().sum())

print("\nCustomer Data Sample:")

print(
    orders_analytics[
        ["order_id", "customer_unique_id", "customer_city", "customer_state"]
    ].head()
)


# 14. Save final analytical dataset
OUTPUT_FILE = PROCESSED_DIR / "order_level_analytics.csv"

orders_analytics.to_csv(
    OUTPUT_FILE,
    index=False
)

print("\nFinal analytical dataset saved successfully!")
print("File:", OUTPUT_FILE)
print("Shape:", orders_analytics.shape)
