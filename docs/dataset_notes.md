# Dataset Documentation

## 1. Dataset Name

**Brazilian E-Commerce Public Dataset by Olist**

## 2. Dataset Overview

The Olist Brazilian E-Commerce dataset is a public e-commerce dataset containing information about online orders, customers, products, sellers, payments, and deliveries.

The dataset provides an opportunity to understand how an e-commerce business operates and analyse different aspects of its sales and customer activities.

For this project, the dataset will be used to build an automated sales data pipeline that extracts, processes, validates, and stores data for business intelligence and reporting.

## 3. Dataset Source

- Platform: Kaggle
- Dataset: Brazilian E-Commerce Public Dataset by Olist
- Link: https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce

## 4. Dataset Files

The dataset contains multiple CSV files representing different parts of the e-commerce business.

Some important files include:

| File | Description |
|---|---|
| olist_orders_dataset.csv | Information about customer orders |
| olist_customers_dataset.csv | Customer information |
| olist_order_items_dataset.csv | Products included in each order |
| olist_products_dataset.csv | Product details |
| olist_sellers_dataset.csv | Seller information |
| olist_order_payments_dataset.csv | Payment details |
| olist_order_reviews_dataset.csv | Customer reviews |
| olist_geolocation_dataset.csv | Geographical information |

## 5. Initial Dataset Exploration

The orders dataset was selected for initial exploration.

The following operations were performed using Python and Pandas:

- Loaded the CSV file using `pd.read_csv()`.
- Examined the first five records using `head()`.
- Checked the number of rows and columns using `shape`.
- Inspected column names and data types using `info()`.
- Identified missing values using `isnull().sum()`.

### Orders Dataset Statistics

- Total rows: [Enter your result]
- Total columns: [Enter your result]
- Missing values: [Enter your result]

## 6. Important Columns in the Orders Dataset

| Column | Description |
|---|---|
| order_id | Unique identifier for an order |
| customer_id | Identifier of the customer |
| order_status | Current status of the order |
| order_purchase_timestamp | Date and time when the order was placed |
| order_approved_at | Order approval timestamp |
| order_delivered_carrier_date | Date when the order was handed to the carrier |
| order_delivered_customer_date | Date when the order was delivered to the customer |
| order_estimated_delivery_date | Estimated delivery date |

## 7. Dataset Relationships

The dataset contains multiple related tables connected through common identifiers.

Examples:

- Orders and Customers are connected through `customer_id`.
- Orders and Order Items are connected through `order_id`.
- Order Items and Products are connected through `product_id`.
- Order Items and Sellers are connected through `seller_id`.
- Orders and Payments are connected through `order_id`.

The original dataset schema diagram is saved in this project's documentation folder for reference.

## 8. Initial Observations

During the initial exploration:

- The dataset is divided into multiple CSV files.
- Different files represent different business entities.
- Common identifiers allow information from different tables to be combined.
- The orders dataset contains timestamps that can be used for delivery and sales analysis.
- Missing values need to be investigated before deciding how to handle them.

## 9. Project Objectives Using This Dataset

The dataset will be used to:

1. Develop an automated ETL pipeline.
2. Perform data quality checks and cleaning.
3. Store structured data in PostgreSQL.
4. Design fact and dimension tables.
5. Calculate business KPIs using SQL.
6. Develop interactive Power BI dashboards.
7. Automate pipeline execution and monitor failures.

## 10. Tools Used

- Python
- Pandas
- NumPy
- PostgreSQL (planned)
- SQL (planned)
- Power BI (planned)
- Git and GitHub

---

**Documentation Status:** Initial dataset exploration completed. Further profiling, validation, and transformation will be performed in subsequent development stages.