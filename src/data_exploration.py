
import pandas as pd
from pathlib import Path

# Dataset directory
data_path = Path("data/raw")

# List available CSV files
files = sorted(data_path.glob("*.csv"))

print("Available datasets:")
for file in files:
    print(file.name)

# Load orders dataset
orders = pd.read_csv(data_path / "olist_orders_dataset.csv")

# Basic exploration
print("\nFirst five records:")
print(orders.head())

print("\nDataset dimensions:", orders.shape)

print("\nDataset information:")
orders.info()

print("\nMissing values:")
print(orders.isnull().sum())

