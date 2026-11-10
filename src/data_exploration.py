
import pandas as pd
import os

file_path = "data/raw/"


files = os.listdir(file_path)

print("Available datasets:")

for file in files:
    print(file)

# Load orders dataset
orders = pd.read_csv(
    file_path + "olist_orders_dataset.csv"
)

# Display first five records
print("\nFirst five records:")
print(orders.head())

# Display dataset dimensions
print("\nDataset shape:")
print(orders.shape)

# Display column information
print("\nDataset information:")
print(orders.info())

# Check missing values
print("\nMissing values:")
print(orders.isnull().sum())
